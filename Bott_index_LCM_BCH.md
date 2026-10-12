# Bott index 与 Local Chern marker：BCH 展开的详细解释

这份笔记按原图的推导顺序，说明：

1. 为什么把 Bott index 中的 $U,V$ 写成指数形式？
2. BCH（Baker–Campbell–Hausdorff）公式做了什么，为什么出现交换子 $[X_P,Y_P]$？
3. 为什么改变 $U,V$ 的乘法顺序会改变符号？

**核心结论：** Bott index 的四算符乘积在形式上的最低非零阶展开中包含投影位置算符的交换子 $[P\hat xP,P\hat yP]$，而这个交换子也是 Local Chern marker（LCM）的核心数学结构。

## 一、Bott index 中的 $U$ 和 $V$

博士论文使用的定义是

$$
B=\frac{1}{2\pi}\mathrm{Im}\mathrm{Tr}\log(VUV^\dagger U^\dagger),
$$

其中

$$
U=Pe^{i\frac{2\pi}{L_x}\hat x}P,\qquad
V=Pe^{i\frac{2\pi}{L_y}\hat y}P.
$$

- $P$：占有态投影算符，将 Hilbert 空间中的态投影到占有态子空间。
- $\hat x,\hat y$：两个方向的位置算符。
- $U,V$：经占有态投影的位置相位算符。

例如，若 $\hat x|x_j\rangle=x_j|x_j\rangle$，则

$$
e^{i\frac{2\pi}{L_x}\hat x}|x_j\rangle
=e^{i\frac{2\pi}{L_x}x_j}|x_j\rangle.
$$

即位置相位算符会根据格点坐标赋予不同的复相位。

### 引入 $\epsilon_x,\epsilon_y$

原图定义

$$
\boxed{\epsilon_x=\frac{2\pi}{L_x},\qquad
\epsilon_y=\frac{2\pi}{L_y}.}
$$

于是

$$
U=Pe^{i\epsilon_x\hat x}P,\qquad
V=Pe^{i\epsilon_y\hat y}P.
$$

当 $L_x,L_y\to\infty$，有 $\epsilon_x,\epsilon_y\to0$，因此可以考虑以它们为形式展开参数。

**注意：** $\epsilon_x\to0$ 不自动意味着 $\epsilon_x\hat x\to0$，因为随系统尺寸增大，位置算符的取值范围通常也会增大。原图的近似需要理解为揭示算符结构的形式分析，不能仅由 $L\to\infty$ 证明所有高阶项可忽略。

## 二、为什么引入 $X_P=P\hat xP$？

原图写成

$$
U\simeq e^{i\epsilon_xX_P},\qquad
V\simeq e^{i\epsilon_yY_P},
$$

其中

$$
X_P=P\hat xP,\qquad Y_P=P\hat yP.
$$

指数函数的 Taylor 展开为

$$
e^A=I+A+\frac{A^2}{2!}+\frac{A^3}{3!}+\cdots.
$$

因此

$$
e^{i\epsilon_x\hat x}
=I+i\epsilon_x\hat x-\frac{\epsilon_x^2}{2}\hat x^2+\cdots.
$$

左右乘以 $P$，有

$$
\begin{aligned}
U&=Pe^{i\epsilon_x\hat x}P\\
&=P+i\epsilon_xP\hat xP
-\frac{\epsilon_x^2}{2}P\hat x^2P+\cdots.
\end{aligned}
$$

保留零阶和一阶项：

$$
U=P+i\epsilon_xX_P+O(\epsilon_x^2).
$$

在占有态子空间中，$P$ 起单位算符 $I_{\mathrm{occ}}$ 的作用，故

$$
U=I_{\mathrm{occ}}+i\epsilon_xX_P+O(\epsilon_x^2).
$$

另一方面

$$
e^{i\epsilon_xX_P}
=I_{\mathrm{occ}}+i\epsilon_xX_P+O(\epsilon_x^2).
$$

由于一阶展开相同，原图作形式近似：

$$
\boxed{U\simeq e^{i\epsilon_xX_P},\qquad
V\simeq e^{i\epsilon_yY_P}.}
$$

但这不是严格恒等式，因为一般

$$
P\hat x^2P\ne(P\hat xP)^2.
$$

**第一步的目的：** 将位置相位算符与投影位置算符联系起来。

## 三、为什么需要 BCH 公式？

Bott index 使用四个算符的乘积：

$$
VUV^\dagger U^\dagger.
$$

采用上述指数近似后，需要研究

$$
e^{i\epsilon_yY_P}
e^{i\epsilon_xX_P}
e^{-i\epsilon_yY_P}
e^{-i\epsilon_xX_P}.
$$

不能直接把指数中的项相加并得出乘积为 $I$，因为投影位置算符一般不对易：

$$
[\hat x,\hat y]=0,\qquad
[X_P,Y_P]\ne0\quad\text{（一般情况下）}.
$$

对于不对易算符 $A,B$，通常

$$
e^Ae^B\ne e^{A+B}.
$$

因此，需要 BCH 公式处理指数算符的乘积。

## 四、BCH 公式是什么？

Baker–Campbell–Hausdorff（BCH）公式表示为

$$
e^Ae^B=e^C,
$$

其中

$$
\boxed{C=A+B+\frac12[A,B]
+\frac1{12}[A,[A,B]]
+\frac1{12}[B,[B,A]]+\cdots.}
$$

交换子的定义为

$$
[A,B]=AB-BA.
$$

若 $[A,B]=0$，则恢复普通指数乘法规则 $e^Ae^B=e^{A+B}$。

对于原图中的四指数乘积，使用以下特殊形式（$A,B$ 均作为一阶小量）：

$$
\boxed{
e^Ae^Be^{-A}e^{-B}
=\exp\bigl([A,B]+O(\epsilon^3)\bigr).
}
$$

### 用 Taylor 展开验证

保留至二阶：

$$
\begin{aligned}
e^A&=I+A+\frac{A^2}{2}+O(\epsilon^3),\\
e^B&=I+B+\frac{B^2}{2}+O(\epsilon^3),\\
e^{-A}&=I-A+\frac{A^2}{2}+O(\epsilon^3),\\
e^{-B}&=I-B+\frac{B^2}{2}+O(\epsilon^3).
\end{aligned}
$$

依次相乘并保留到二阶：

$$
e^Ae^Be^{-A}e^{-B}
=I+AB-BA+O(\epsilon^3)
=I+[A,B]+O(\epsilon^3).
$$

由于 $[A,B]$ 已经是二阶小量，可再写成

$$
e^Ae^Be^{-A}e^{-B}
=\exp\bigl([A,B]+O(\epsilon^3)\bigr).
$$

**这解释了为什么四个指数中一阶项相互抵消，但二阶交换子仍然留下。**

## 五、应用于论文所用的 Bott index 顺序

令

$$
A=i\epsilon_xX_P,\qquad D=i\epsilon_yY_P.
$$

于是

$$
U\simeq e^A,\qquad V\simeq e^D,
$$

并且

$$
VUV^\dagger U^\dagger
\simeq e^De^Ae^{-D}e^{-A}.
$$

BCH 公式给出

$$
e^De^Ae^{-D}e^{-A}
=\exp\bigl([D,A]+O(\epsilon^3)\bigr).
$$

现在逐项求交换子：

$$
\begin{aligned}
DA&=(i\epsilon_yY_P)(i\epsilon_xX_P)
=-\epsilon_x\epsilon_yY_PX_P,\\
AD&=(i\epsilon_xX_P)(i\epsilon_yY_P)
=-\epsilon_x\epsilon_yX_PY_P,\\
[D,A]&=DA-AD\\
&=\epsilon_x\epsilon_y(X_PY_P-Y_PX_P)\\
&=\epsilon_x\epsilon_y[X_P,Y_P].
\end{aligned}
$$

因此

$$
\boxed{
VUV^\dagger U^\dagger
\simeq\exp\left(
+\epsilon_x\epsilon_y[X_P,Y_P]+O(\epsilon^3)
\right).
}
$$

这个正号很重要，因为论文所用的 LCM 也含有 $+[X_P,Y_P]$。

## 六、为什么改变算符顺序会得到负号？

若采用

$$
UVU^\dagger V^\dagger
\simeq e^Ae^De^{-A}e^{-D},
$$

BCH 给出

$$
e^Ae^De^{-A}e^{-D}
=\exp\bigl([A,D]+O(\epsilon^3)\bigr).
$$

而

$$
[A,D]=-[D,A]
=-\epsilon_x\epsilon_y[X_P,Y_P].
$$

因此

$$
\boxed{
UVU^\dagger V^\dagger
\simeq\exp\left(
-\epsilon_x\epsilon_y[X_P,Y_P]+O(\epsilon^3)
\right).
}
$$

| Bott 算符顺序 | BCH 展开的交换子 |
|---|---|
| $VUV^\dagger U^\dagger$ | $+\epsilon_x\epsilon_y[X_P,Y_P]$ |
| $UVU^\dagger V^\dagger$ | $-\epsilon_x\epsilon_y[X_P,Y_P]$ |

所以交换 $U,V$ 的顺序会反转最低阶交换子的符号。

## 七、这与 Local Chern marker 有什么关系？

论文中的 LCM 定义为

$$
\mathfrak C(\boldsymbol r)
=2\pi\mathrm{Im}\langle\boldsymbol r|
P\hat xP\hat yP-P\hat yP\hat xP
|\boldsymbol r\rangle.
$$

因为

$$
X_P=P\hat xP,\qquad Y_P=P\hat yP,
$$

所以直接得到严格的代数恒等式：

$$
\boxed{
\mathfrak C(\boldsymbol r)
=2\pi\mathrm{Im}
\langle\boldsymbol r|[X_P,Y_P]|\boldsymbol r\rangle.
}
$$

对比：

**Bott index 的形式展开**

$$
VUV^\dagger U^\dagger
\sim e^{+\epsilon_x\epsilon_y[X_P,Y_P]+\cdots}.
$$

**LCM 的严格表达式**

$$
\mathfrak C(\boldsymbol r)
=2\pi\mathrm{Im}\langle\boldsymbol r|
[X_P,Y_P]|\boldsymbol r\rangle.
$$

共同的数学结构是

$$
\boxed{[X_P,Y_P]=[P\hat xP,P\hat yP].}
$$

Bott index 通过指数算符的闭合乘积描述全局拓扑性质；LCM 则使用交换子的局部矩阵元表示空间分布。两者具有相同的交换子方向。

但**不能仅凭 BCH 形式展开就断言完整 Bott index 等于 LCM 的 bulk 平均**。有限维空间中有

$$
\mathrm{Tr}[X_P,Y_P]=0,
$$

而 Bott index 可以非零。这还涉及矩阵对数的分支信息，以及合适的有限尺寸、局域性等条件。

此外，$U\simeq e^{i\epsilon_xX_P}$ 已舍弃投影产生的高阶修正，因此 BCH 的 $O(\epsilon^3)$ 不能未经证明就视为原始投影算符乘积的完整误差。

## 八、整张图片的一句话总结

$$
\boxed{
\begin{gathered}
U\simeq e^{i\epsilon_xX_P},\qquad
V\simeq e^{i\epsilon_yY_P}\\[5pt]
\Downarrow\quad\text{BCH 展开}\\[5pt]
VUV^\dagger U^\dagger
\sim e^{+\epsilon_x\epsilon_y[X_P,Y_P]}\\[5pt]
\Downarrow\\[5pt]
\mathfrak C(\boldsymbol r)
=2\pi\mathrm{Im}
\langle\boldsymbol r|[X_P,Y_P]|\boldsymbol r\rangle
\end{gathered}
}
$$

**BCH 公式的作用是把 Bott index 中四个指数算符的乘积，联系到投影位置算符的交换子，从而帮助理解它与 LCM 的关系。** 这个形式展开不是两种指标数值严格等价的证明。
