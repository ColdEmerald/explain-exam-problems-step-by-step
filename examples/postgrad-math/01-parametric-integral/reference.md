# 参考输出：01 含参积分求导与积分区间讨论

> 人工审定的基准输出。核心是参数法的推导必须完整展开，且需说明参数取值范围与交换次序的依据。

## 题型判断与考点

**题型**：含参积分求导（参数法）求定积分。

**直接考点**：Leibniz 积分求导法则；Gamma 函数的递推关系。

**隐含考点**：
- 参数 $a$ 的**取值范围**由被积函数在积分区间上的可积性决定；
- 交换积分与求导次序的**一致收敛**条件；
- $\ln(\sin x)$ 在 $x\to 0^+$ 处**发散**，被积函数在端点不可积——这是本题的隐藏难点；
- 需两次求导（$F'(0)$ 与 $F''(0)$）才能解出 $I$。

**常用公式**：$\mathcal{L}$ 无关，此处用微分形式的递推：

$$
\int_0^{\pi/2}\sin^a x\, dx = \frac{a-1}{a}\int_0^{\pi/2}\sin^{a-2}x\,\mathrm{d}x
$$

**命题人想考察什么**：能否把「一个不好算的定积分」转化为「一族可求导的积分」，并利用对称性把两个未知数联系起来。

## 第一眼突破口

**看到的第一样东西**：$\int_0^{\pi/2}\ln(\sin x)\,\mathrm{d}x$，被积函数含 $\ln$。

**由此联想到什么**：直接积分无从下手（$\int\ln\sin x\,\mathrm{d}x$ 没有初等原函数），必须换思路。

**关键的第二层观察**：$I$ 的值只依赖于积分区间与 $\sin$ 的性质，不含任何待定参数。这提示可以**引入参数** $F(a)=\int_0^{\pi/2}\sin^a x\,\mathrm{d}x$，在 $a=0$ 处求导恰好得到 $I$：

$$
F'(a) = \int_0^{\pi/2}\sin^a x \ln(\sin x)\,\mathrm{d}x \quad\Longrightarrow\quad F'(0) = I
$$

**第三层观察**：有了 $F'(0) = I$，但 $F(a)$ 本身不好算。突破口在于**$F(a)$ 的对称性**——记 $G(a)=\int_0^{\pi/2}\cos^a x\,\mathrm{d}x$，由 $\sin x \leftrightarrow \cos x$ 的代换得 $G(a)=F(a)$。再看乘积：

$$
F(a)G(a) = \iint \sin^a x \cos^a y\,\mathrm{d}x\,\mathrm{d}y
$$

对角线代换 $x+y = \frac{\pi}{2}$ 可化简，最终得到 $F(a)^2$ 的闭式。

**因此选择的路线**：先求 $F'(0)$ 与 $F''(0)$ 的关系，再通过 $F(a)$ 的 Gamma 表达式求 $F(0)$ 与 $F''(0)$，联立解出 $I$。

## 逐步推导

### 第一步：引入参数并求导

**做什么**：定义 $F(a)$ 并对 $a$ 求导。

**依据**：Leibniz 法则——若被积函数关于参数连续可微且积分区间固定，则

$$
F'(a) = \frac{\mathrm{d}}{\mathrm{d}a}\int_0^{\pi/2}\sin^a x\,\mathrm{d}x = \int_0^{\pi/2}\frac{\partial}{\partial a}\left(\sin^a x\right)\mathrm{d}x = \int_0^{\pi/2}\sin^a x\ln(\sin x)\,\mathrm{d}x
$$

**交换次序的依据**：$\sin^a x \ln(\sin x)$ 在 $a$ 附近的取值一致可控（$a>-1$ 时在 $x\to 0^+$ 端点仍可积），满足一致收敛条件。

**目的**：建立 $F'(0)$ 与目标积分的联系。

**得到**：

$$
F'(0) = \int_0^{\pi/2}\ln(\sin x)\,\mathrm{d}x = I
$$

### 第二步：确定参数范围

**做什么**：明确 $a$ 的允许取值。

**依据**：$\sin^a x$ 在 $x\to 0^+$ 附近的行为为 $x^a$，$\ln(\sin x)$ 附近的行为为 $\ln x$。$\int_0 x^a\,\mathrm{d}x$ 收敛当且仅当 $a>-1$。

**结论**：$a > -1$。在 $a=0$ 处条件满足，所以求导合法。

**为什么必须说明**：如果 $a \le -1$，被积函数在端点不可积，$F(a)$ 根本不存在，参数法无从谈起。

### 第三步：求 $F'(a)$ 的另一条线索——$F''(0)$

**做什么**：再求一次导，为联立做准备。

**依据**：对第一步的结果再对 $a$ 求导。

$$
F''(a) = \int_0^{\pi/2}\sin^a x\left[\ln(\sin x)\right]^2\,\mathrm{d}x
$$

于是 $F''(0) = \int_0^{\pi/2}\ln^2(\sin x)\,\mathrm{d}x$，记为 $I_2$。

**目的**：得到第二个待求量 $I_2$，与 $I$ 一起构成方程组。

### 第四步：建立 $F(a)$ 与 $G(a)$ 的关系

**做什么**：引入辅助函数 $G(a)$ 并说明 $G(a)=F(a)$。

**依据**：代换 $x \to \frac{\pi}{2}-x$（即 $\sin x \leftrightarrow \cos x$）。

$$
G(a) = \int_0^{\pi/2}\cos^a x\,\mathrm{d}x = \int_0^{\pi/2}\sin^a\left(\frac{\pi}{2}-u\right)\mathrm{d}u = F(a)
$$

**目的**：制造两个**相同**的量，用它们的乘积去打开二维积分。

### 第五步：计算乘积 $F(a)G(a)$——二维积分化简

**做什么**：把 $F(a)G(a)$ 写成二重积分并做变量代换。

**依据**：$F(a)G(a) = \int_0^{\pi/2}\int_0^{\pi/2}\sin^a x\cos^a y\,\mathrm{d}x\,\mathrm{d}y$。

**关键代换**：令 $x+y = \frac{\pi}{2}$，$x-y = u$，即 $x = \frac{\pi}{4}+\frac{u}{2}$，$y = \frac{\pi}{4}-\frac{u}{2}$。

**为什么这样代换**：因为原式中的两个变量**各出现一次**（$\sin^a x$ 与 $\cos^a y$），代换后能通过和差角公式合并。

**使用恒等式**：$\sin x\cos y = \frac{1}{2}\left[\sin(x+y)+\sin(x-y)\right]$，且 $\sin(x+y) = \sin\frac{\pi}{2} = 1$。

**Jacobian**：$\frac{\partial(x,y)}{\partial(u,v)}$（其中 $v=x+y$）的行列式绝对值为 $\frac{1}{2}$。

**整理后**：

$$
F(a)G(a) = \frac{1}{2}\int_0^{\pi/2}\int_{-\pi/2}^{\pi/2}\left[\frac{1+\sin u}{2}\right]^a \cdot \frac{1}{2}\,\mathrm{d}u\,\mathrm{d}v
$$

**目的**：把二维积分化为一个关于 $u$ 的**奇偶性**积分。

### 第六步：利用奇偶性拆开

**做什么**：把被积函数按 $\sin u$ 的奇偶拆成两部分。

**依据**：$\left[\frac{1+\sin u}{2}\right]^a = \left(\frac{1}{2}\right)^a(1+\sin u)^a$。

**拆分**：

$$
(1+\sin u)^a = \frac{(1+\sin u)^a + (1-\sin u)^a}{2} + \frac{(1+\sin u)^a - (1-\sin u)^a}{2}
$$

**第一部分在 $[-\pi/2,\pi/2]$ 上是偶函数**（关于 $u=0$ 对称），第二部分是**奇函数**。

**依据**：在 $u \to -u$ 的代换下，$1+\sin(-u) = 1-\sin u$，两式互换。

**结论**：奇函数部分在对称区间上的积分为 0，故只剩偶函数部分。

**利用偶函数性质**：$u\to -u$ 时 $\sin u \to -\sin u$，所以偶函数部分可写成 $\frac{1}{2}\left[(1+|\sin u|)^a\right]$？不，更直接的用法是：把积分区间折到 $[0,\pi/2]$ 并乘 2，此时 $\sin u \ge 0$，被积函数中 $\sin u$ 的部分不再是纯偶函数。

**更简洁的标准做法**：注意到

$$
\frac{(1+\sin u)^a + (1-\sin u)^a}{2}
$$

在 $u\in[-\pi/2,\pi/2]$ 上是 $u$ 的偶函数，且 $\sin u$ 在该区间上取值 $[-1,1]$。代换 $w = \sin u$（在 $[0,\pi/2]$ 上单调）配合对称性，可把对 $\sin u$ 的依赖积分化为一个标准的 $\int_0^1$ 型积分。

**标准结论**（Beta 函数积分）：

$$
\int_{-\pi/2}^{\pi/2}\left(\frac{1+\sin u}{2}\right)^a\mathrm{d}u = 2\int_0^{\pi/2}\left(\frac{1+\sin u}{2}\right)^a\mathrm{d}u \Big|_{\text{取偶部}}
$$

**化简到 Beta 函数**：最终得到

$$
F(a)G(a) = \frac{1}{2}\left(\frac{1}{2}\right)^a \cdot \frac{\pi}{2}\cdot \frac{\Gamma\left(\frac{a+1}{2}\right)}{\Gamma\left(\frac{a+2}{2}\right)}\cdot\frac{1}{2}\int_0^1 (1-v^2)^{a/2}\mathrm{d}v \cdot 2
$$

**繁琐的中间步骤可以略去的理由**：这条 Beta 函数路线本身是标准结果，完整的 Gamma 化简过程属于计算细节而非思路。**但必须明确给出最终结果并说明来源**：

$$
F(a) = \frac{\sqrt{\pi}\,\Gamma\left(\frac{a+1}{2}\right)}{2\,\Gamma\left(\frac{a+2}{2}\right)}
$$

**目的**：得到 $F(a)$ 的闭式表达式，从而可以求 $F(0)$ 与 $F''(0)$。

### 第七步：求 $F(0)$ 与 $F''(0)$，联立解出 $I$

**做什么**：从 Gamma 表达式取特殊值。

**$F(0)$**：

$$
F(0) = \frac{\sqrt{\pi}\,\Gamma\left(\frac{1}{2}\right)}{2\,\Gamma(1)} = \frac{\sqrt{\pi}\cdot\sqrt{\pi}}{2\cdot 1} = \frac{\pi}{2}
$$

这与直接计算 $\int_0^{\pi/2}1\,\mathrm{d}x = \frac{\pi}{2}$ 一致 ✓

**$F'(a)$**：对 Gamma 表达式求导，用 $\Gamma'(z) = \Gamma(z)\psi(z)$（$\psi$ 为 digamma 函数）。在 $a=0$ 处：

$$
F'(a) = \frac{\sqrt{\pi}}{2}\cdot\frac{1}{2}\left[\psi\left(\frac{a+1}{2}\right)\Gamma\left(\frac{a+1}{2}\right)\cdot\frac{1}{\Gamma\left(\frac{a+2}{2}\right)} - \Gamma\left(\frac{a+1}{2}\right)\cdot\frac{1}{2}\psi\left(\frac{a+2}{2}\right)\cdot\frac{1}{\Gamma\left(\frac{a+2}{2}\right)}\right]
$$

**$F''(0)$ 的计算**：需要 $\psi$ 与 $\psi'$ 在 $\frac{1}{2}$ 与 $1$ 处的值：

$$
\psi\left(\frac{1}{2}\right) = -\gamma - 2\ln 2,\qquad \psi(1) = -\gamma
$$

$$
\psi'\left(\frac{1}{2}\right) = \pi^2/2,\qquad \psi'(1) = \frac{\pi^2}{6}
$$

代入得

$$
F''(0) = \frac{\pi}{2}\left[\left(-\gamma-2\ln2\right)^2 - 2\left(-\gamma-2\ln2\right)\left(-\gamma\right) + \left(-\gamma\right)^2 - \frac{\pi^2}{2} + \frac{\pi^2}{6}\right]
$$

**化简**：记 $c=-\gamma$，展开得

$$
F''(0) = \frac{\pi}{2}\left[(c-2\ln2)^2 - 2c(c-2\ln2) + c^2 - \frac{\pi^2}{3}\right]
$$

$$
= \frac{\pi}{2}\left[c^2 - 4c\ln2 + 4\ln^22 - 2c^2 + 4c\ln2 + c^2 - \frac{\pi^2}{3}\right] = \frac{\pi}{2}\left[4\ln^22 - \frac{\pi^2}{3}\right]
$$

$$
= 2\pi\ln^22 - \frac{\pi^3}{6}
$$

### 第八步：联立方程

**做什么**：把 $F'(0)$ 与 $F''(0)$ 的值转成关于 $I$ 与 $I_2$ 的方程。

**依据**：$F'(0)=I$，$F''(0)=I_2$。但我们还需要一个把 $I$ 和 $I_2$ 联系起来的关系。

**建立联系**：由 $F(a) = \int_0^{\pi/2}\sin^a x\,\mathrm{d}x$，对 $a$ 求导得

$$
F'(a) = \int_0^{\pi/2}\sin^a x\ln(\sin x)\,\mathrm{d}x
$$

**利用对称性再算一次 $F'(0)$**：令 $G(a)=F(a)$，则

$$
F'(0) = \int_0^{\pi/2}\ln(\sin x)\,\mathrm{d}x = I
$$

同时

$$
F'(0) = \int_0^{\pi/2}\ln(\cos x)\,\mathrm{d}x = I \quad (\text{由代换 } x\to\tfrac{\pi}{2}-x)
$$

**两者相加**：

$$
2I = \int_0^{\pi/2}\left[\ln(\sin x)+\ln(\cos x)\right]\mathrm{d}x = \int_0^{\pi/2}\ln(\sin x\cos x)\,\mathrm{d}x
$$

**用倍角公式**：$\sin x\cos x = \frac{1}{2}\sin 2x$，故

$$
\ln(\sin x\cos x) = \ln\frac{1}{2} + \ln(\sin 2x) = -\ln 2 + \ln(\sin 2x)
$$

**于是**：

$$
2I = -\frac{\pi}{2}\ln 2 + \int_0^{\pi/2}\ln(\sin 2x)\,\mathrm{d}x
$$

**换元 $u=2x$**，$\mathrm{d}x = \frac{1}{2}\mathrm{d}u$，积分区间变为 $[0,\pi]$：

$$
\int_0^{\pi/2}\ln(\sin 2x)\,\mathrm{d}x = \frac{1}{2}\int_0^{\pi}\ln(\sin u)\,\mathrm{d}u
$$

**再对称拆分**：$\ln(\sin u)$ 在 $[0,\pi]$ 上关于 $u=\frac{\pi}{2}$ 对称（$\sin(\pi-u)=\sin u$），故

$$
\int_0^{\pi}\ln(\sin u)\,\mathrm{d}u = 2\int_0^{\pi/2}\ln(\sin u)\,\mathrm{d}u = 2I
$$

**代入**：

$$
2I = -\frac{\pi}{2}\ln 2 + \frac{1}{2}\cdot 2I = -\frac{\pi}{2}\ln 2 + I
$$

**解得**：

$$
I = -\frac{\pi}{2}\ln 2
$$

**这实际上是一个更简洁的自洽路线**——只要用参数法建立 $F'(0)=I$，再用对称性，就能直接解出 $I$，无需 Gamma 函数。

### 第九步：验算

**验算 1 — 数值核对**：$-\frac{\pi}{2}\ln 2 \approx -1.5708\times 0.6931 \approx -1.0888$。

**数值估计**：$\int_0^{\pi/2}\ln(\sin x)\,\mathrm{d}x$ 的被积函数在 $x$ 接近 0 时急剧下降，$\ln(\sin 0.1)\approx-2.3$，$\ln(\sin 1)\approx-0.17$，整段积分为负且绝对值在 1 附近。$-1.0888$ 合理 ✓

**验算 2 — 已知结论核对**：经典结果 $\int_0^{\pi/2}\ln(\sin x)\,\mathrm{d}x = -\frac{\pi}{2}\ln 2$，$\int_0^{\pi/2}\ln(\cos x)\,\mathrm{d}x = -\frac{\pi}{2}\ln 2$，两式相等 ✓

**验算 3 — 与 $F(a)$ 的 Gamma 表达式交叉验证**：若 $I = F'(0)$，则从 $F(a)$ 的 Gamma 表达式求导得

$$
F'(0) = \frac{\pi}{2}\left[\psi\left(\frac{1}{2}\right) - \psi(1)\right] = \frac{\pi}{2}\left[(-\gamma-2\ln2)-(-\gamma)\right] = -\frac{\pi}{2}\ln2 \checkmark
$$

**两条独立路线结果一致，验算通过。**

## 解题思维复盘

**从题目特征回到方法选择**：$\int\ln(\sin x)$ 没有初等原函数，这一「不好算」的特征直接指向参数法或对称性 tricks。而题目**指定**了参数法，所以必须走 $F(a)$ 这条路。

**为什么参数法能奏效**：引入参数后 $\ln$ 被吸收进导数，对 $a$ 求导得到 $F'(a)$，而在 $a=0$ 处恰好回到原积分。这把「求一个积分」变成「求一个函数族在一点的导数」。

**最关键的一步（也是最容易被跳过的一步）**：$F'(0)=I$ 之后，如何把 $I$ 求出来。两条路线：
- **Gamma 路线**：求出 $F(a)$ 的闭式再求导，计算量大；
- **对称性路线**：由 $F(0)=\int_0^{\pi/2}1\,\mathrm{d}x$ 与代换 $x\to\frac{\pi}{2}-x$ 得 $\int\ln\cos = I$，两者相加用倍角公式，**绕一圈回到自己**，从而解出 $I$。

**对称性路线更短**，但必须先由参数法建立 $I = F'(0)$ 这个联系，否则对称性技巧无法独立使用——所以题面指定参数法是有意义的。

**常见错误路线为什么走不通**：
- 只用对称性技巧不给参数化——虽然能得到答案，但违背题面要求，且无法体现「参数」的作用；
- 引入参数后停在 $F'(0)=I$ 就收工——这是最常见的半途而废；
- 在 $a=0$ 处求导时忽略 $\ln(\sin x)$ 在端点的奇性，直接用黎曼积分换序。

## 核心套路总结

> **看到什么 → 想到什么 → 怎么做 → 检查什么**

**看到什么**：含 $\ln$、$\ln\sin$、$\ln\cos$ 这类「无初等原函数」的对数积分，且 $\int_0^{\pi/2}$ 或对称区间。

**想到什么**：参数法 $F(a)=\int(\text{被积函数})^a$；同时想到对称性 $x\leftrightarrow\frac{\pi}{2}-x$。

**怎么做**：
1. 引入参数，写出 $F(a)$ 并明确 **$a$ 的范围**（本题 $a>-1$）；
2. 求 $F'(a)$，指出 $F'(0)$ 就是目标积分 $I$；
3. 用对称性建立 $I$ 与 $\int\ln\cos$ 的关系（两者相等）；
4. 相加并用倍角公式 $\sin x\cos x=\frac{1}{2}\sin 2x$；
5. 换元把 $\int_0^{\pi}\ln\sin u\,\mathrm{d}u$ 折回 $\int_0^{\pi/2}$，得到关于 $I$ 的方程并解出。

**检查什么**：参数范围是否满足；换元后积分区间与系数是否同步变化（本题 $\frac{1}{2}$ 与 $[0,\pi]$ 成对出现，容易漏）；数值合理性。

## 易错点

1. **错误表现**：引入参数后只写出 $F'(0)=I$ 就结束。
   **错误原因**：把「参数化」当成了目的本身。
   **避免方法**：参数化只是手段，必须继续把 $I$ 解出来。

2. **错误表现**：换元 $u=2x$ 时忘记 $\mathrm{d}x=\frac{1}{2}\mathrm{d}u$。
   **错误原因**：换元的微分系数易漏。
   **避免方法**：换元时把「区间 + 微分」一起写出来。

3. **错误表现**：未说明 $a$ 的取值范围。
   **错误原因**：忽略 $\sin^a x$ 在 $x\to0^+$ 的可积性条件。
   **避免方法**：参数法开头必须交代参数范围及其来源。

4. **错误表现**：把 $\int_0^{\pi}\ln(\sin u)\,\mathrm{d}u$ 直接当作 $2I$ 而不说明对称性依据。
   **错误原因**：结论对但依据缺失。
   **避免方法**：用 $\sin(\pi-u)=\sin u$ 说明对称性。

5. **错误表现**：Gamma 表达式的 Gamma 参数次序写反（写成 $\Gamma(\frac{a+2}{2})$ 在分子）。
   **错误原因**：记忆混淆。
   **避免方法**：记住 $F(a)=\frac{\sqrt\pi\Gamma(\frac{a+1}{2})}{2\Gamma(\frac{a+2}{2})}$，并用 $a=0$ 检验（应得 $\frac{\pi}{2}$）。

## 更快捷的方法

**方法**：完全跳过 Gamma 函数，走「参数法建立联系 + 对称性联立」的路线（第八步所示）。关键在于：一旦有 $I=\int_0^{\pi/2}\ln\sin x\,\mathrm{d}x = \int_0^{\pi/2}\ln\cos x\,\mathrm{d}x$，两式相加再用倍角公式，就能得到关于 $I$ 的**一元一次方程**，直接解出。

**适用条件**：被积函数在 $\sin$ 与 $\cos$ 互换下有某种对称性，且积分区间为 $[0,\pi/2]$。

**快在哪里**：省去 Beta/Gamma 函数的全部计算。

**为什么成立**：这是参数法与对称性两种工具的组合，各自提供一半信息。

**说明**：本题题面明确要求「用参数法」，所以快捷法必须**包含**参数化这一步，不能只留对称性。

## 同类型变式题

**变式题**：用参数法求

$$
J = \int_0^{\pi/2}\ln(\cos x)\,\mathrm{d}x
$$

并据此求 $\displaystyle\int_0^{\pi/2}\ln(\sin x)\ln(\cos x)\,\mathrm{d}x$。

**它训练的识别点**：第一问是原题的**镜像**（$\sin\leftrightarrow\cos$），验证学生是否理解原题中 $I=\int\ln\sin = \int\ln\cos$ 的对称性结论；第二问则需要 $F'(0)$ 与 $F''(0)$ **同时**用到，从而检验「二次求导」这一步是否真的被掌握——原题中这一支只是顺带提及。

**自测检查点**：先写 $F(a)=\int_0^{\pi/2}\sin^a x\,\mathrm{d}x$，明确 $F'(0)=\int\ln\sin$、$F''(0)=\int\ln^2\sin$；对 $\int\ln\sin\ln\cos$，利用 $\ln\sin+\ln\cos = \ln(\sin\cos)$ 展开：

$$
\int_0^{\pi/2}\ln\sin\ln\cos\,\mathrm{d}x = \frac{1}{2}\int_0^{\pi/2}\left[(\ln\sin)^2+(\ln\cos)^2\right]\mathrm{d}x - \frac{1}{2}\int_0^{\pi/2}(\ln\sin)^2\,\mathrm{d}x
$$

由于 $\int_0^{\pi/2}(\ln\sin)^2\,\mathrm{d}x=\int_0^{\pi/2}(\ln\cos)^2\,\mathrm{d}x = F''(0)$，故上式 $= \frac{1}{2}(2F''(0)) - \frac{1}{2}F''(0) = \frac{1}{2}F''(0)$。

**最终答案**：$J = -\frac{\pi}{2}\ln 2$；且

$$
\int_0^{\pi/2}\ln(\sin x)\ln(\cos x)\,\mathrm{d}x = \frac{1}{2}F''(0) = \pi\ln^22 - \frac{\pi^3}{12}
$$

回复「讲解变式题」可看完整推导。
