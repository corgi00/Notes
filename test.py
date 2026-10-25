#!/usr/bin/env python3
"""OneNote-exported PDF -> auditable RAG-ready text (plus PDF attachments).

Usage:
  pip install pymupdf
  python onenote_pdf_to_lightrag.py input.pdf --out output
  pip install docling
  python onenote_pdf_to_lightrag.py input.pdf --out output --engine docling

This tool NEVER uploads data. Note: some Docling models may need a first-time download.
It is a prototype, not a production security / compliance control.
PyMuPDF is AGPL-3.0 or commercially licensed; review enterprise licensing.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from collections import deque
from pathlib import Path

import pymupdf

PDF_HEADER = b"%PDF-"
MAX_ATTACHMENT_BYTES = 50 * 1024 * 1024
MAX_FILES = 100


def safe_filename(name: str, fallback: str) -> str:
    # Use only the basename, and remove control/shell/path characters.
    name = str(name or fallback).replace("\\", "/").split("/")[-1]
    name = re.sub(r'[^\w.\-\u3040-\u30ff\u3400-\u9fff]', '_', name, flags=re.UNICODE)
    name = name.strip(". _")[:100]
    return name or fallback


def is_pdf(blob: bytes) -> bool:
    return PDF_HEADER in blob[:1024]


def attachment_candidates(document: pymupdf.Document):
    """Yield (description, attachment bytes) from both PDF attachment mechanisms."""
    for idx, name in enumerate(document.embfile_names()):
        try:
            yield f"embedded_{idx+1}_{name}", document.embfile_get(name)
        except Exception as exc:
            print(f"  [WARN] Could not extract embedded file {name}: {exc}")
    for page_no, page in enumerate(document, 1):
        for annot in page.annots() or []:
            if annot.type[1] != "FileAttachment":
                continue
            try:
                info = annot.file_info or {}
                name = info.get("filename") or info.get("ufilename") or "attachment.bin"
                yield f"page_{page_no}_annotation_{name}", annot.get_file()
            except Exception as exc:
                print(f"  [WARN] Could not extract annotation on page {page_no}: {exc}")


def text_from_pdf(doc: pymupdf.Document, source: str):
    pages = []
    inventory = []
    for page_no, page in enumerate(doc, 1):
        text = page.get_text("text", sort=True).strip()
        # An image count is indicative, but not conclusive: PDFs can use form XObjects/vector art.
        image_count = len(page.get_images(full=True))
        low_text = len(text) < 50
        inventory.append({
            "source_pdf": source, "page": page_no,
            "extracted_characters": len(text), "image_xobjects": image_count,
            "needs_visual_review": low_text,
            "reason": "little text; images detected" if low_text and image_count else
                      "little text; check PDF visually" if low_text else ""
        })
        pages.append(f"[SOURCE: {source} | PAGE: {page_no}]\n{text or '[NO EXTRACTABLE TEXT: inspect page / OCR]'}")
    return "\n\n".join(pages) + "\n", inventory


def parse_docling(path: Path, source: str) -> str:
    from docling.document_converter import DocumentConverter
    converted = DocumentConverter().convert(str(path)).document
    # Markdown formatting intentionally remains in the .txt file; LightRAG will read it as text.
    return f"[SOURCE DOCUMENT: {source}]\n\n" + converted.export_to_markdown() + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path, help="OneNote-exported PDF")
    parser.add_argument("--out", type=Path, default=Path("handover_output"))
    parser.add_argument("--engine", choices=("basic", "docling"), default="basic")
    parser.add_argument("--max-depth", type=int, default=2, help="Nested PDF attachment depth (default 2)")
    args = parser.parse_args()

    if not args.pdf.is_file():
        parser.error(f"No PDF found at: {args.pdf}")
    if args.max_depth < 0:
        parser.error("--max-depth cannot be negative")

    out = args.out.resolve()
    txt_dir = out / "rag_txt"
    att_dir = out / "attachments"
    txt_dir.mkdir(parents=True, exist_ok=True)
    att_dir.mkdir(parents=True, exist_ok=True)

    queue = deque([(args.pdf.resolve(), 0, "original")])
    seen = set()
    pdf_records, page_records, attachment_records = [], [], []
    errors = []
    attachment_count = 0
    while queue:
        pdf_path, depth, parent = queue.popleft()
        if len(pdf_records) >= MAX_FILES:
            errors.append("MAX_FILES cap reached; remaining documents skipped")
            break
        try:
            digest = hashlib.sha256(pdf_path.read_bytes()).hexdigest()
            if digest in seen:
                continue
            seen.add(digest)
            doc = pymupdf.open(str(pdf_path))
            if doc.needs_pass:
                errors.append(f"Password-protected PDF skipped: {pdf_path.name}")
                doc.close()
                continue
            source_name = safe_filename(pdf_path.name, f"document_{len(pdf_records)+1}.pdf")
            unique_id = digest[:10]
            source_tag = f"{source_name} (SHA256:{unique_id})"
            raw_text, pages = text_from_pdf(doc, source_tag)
            page_records.extend(pages)
            attachments = list(attachment_candidates(doc)) if depth < args.max_depth else []
            doc.close()

            selected_engine = args.engine
            result = raw_text
            if args.engine == "docling":
                try:
                    result = parse_docling(pdf_path, source_tag)
                except Exception as exc:
                    selected_engine = "basic (docling failed)"
                    errors.append(f"Docling failed on {source_name}: {type(exc).__name__}: {exc}")
            target = txt_dir / f"{Path(source_name).stem}_{unique_id}.txt"
            target.write_text(result, encoding="utf-8")
            pdf_records.append({
                "file": str(pdf_path), "parent": parent, "depth": depth, "pages": len(pages),
                "characters_basic": sum(p["extracted_characters"] for p in pages),
                "pages_need_visual_review": sum(bool(p["needs_visual_review"]) for p in pages),
                "engine": selected_engine, "output_txt": str(target),
                "attachment_objects_found": len(attachments)
            })
            print(f"[OK] {source_name}: {len(pages)} pages -> {target.name}")

            for a_name, blob in attachments:
                attachment_count += 1
                rec = {"parent_pdf": source_tag, "name": a_name, "bytes": len(blob),
                       "type": "pdf" if is_pdf(blob) else "other", "saved": "", "depth": depth+1}
                if len(blob) > MAX_ATTACHMENT_BYTES:
                    rec["status"] = "skipped: over 50 MiB"
                    attachment_records.append(rec)
                    continue
                ext = ".pdf" if is_pdf(blob) else Path(a_name).suffix or ".bin"
                name = safe_filename(Path(a_name).stem, "attachment")
                a_digest = hashlib.sha256(blob).hexdigest()[:10]
                att_path = att_dir / f"{name}_{a_digest}{ext}"
                att_path.write_bytes(blob)
                rec["saved"] = str(att_path)
                rec["status"] = "saved; queued for parsing" if rec["type"] == "pdf" else "saved; not parsed"
                attachment_records.append(rec)
                if rec["type"] == "pdf":
                    queue.append((att_path, depth + 1, source_tag))
        except Exception as exc:
            errors.append(f"Failed: {pdf_path.name}: {type(exc).__name__}: {exc}")

    summary = {
        "pdfs_processed": len(pdf_records),
        "total_pdf_pages": sum(r["pages"] for r in pdf_records),
        "low_text_pages_needing_review": sum(r["pages_need_visual_review"] for r in pdf_records),
        "pdf_attachments_detected": sum(a["type"] == "pdf" for a in attachment_records),
        "other_attachments_detected": sum(a["type"] != "pdf" for a in attachment_records),
        "total_basic_extracted_characters": sum(r["characters_basic"] for r in pdf_records),
        "txt_files_created": len(pdf_records),
        "errors": errors,
        "caution": "Low-text detection is a screening heuristic; manual OCR/quality review remains essential."
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    (out / "pdf_inventory.json").write_text(json.dumps(pdf_records, indent=2, ensure_ascii=False), encoding="utf-8")
    (out / "attachments_inventory.json").write_text(json.dumps(attachment_records, indent=2, ensure_ascii=False), encoding="utf-8")
    with (out / "pages_to_review.csv").open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=["source_pdf", "page", "extracted_characters", "image_xobjects", "needs_visual_review", "reason"])
        writer.writeheader()
        writer.writerows(page_records)
    print("\n--- Summary ---")
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    print(f"\nImport files under {txt_dir} into your current LightRAG demo.")


if __name__ == "__main__":
    main()
