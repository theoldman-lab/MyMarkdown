# 第五章：实函数向复数域的扩展

## 1. 解析延拓方法

### 1.1 幂级数定义：从实数到复数的桥梁

#### 问题的提出

我们熟悉的实函数，如 $e^x$、$\sin x$、$\cos x$ 等，都是定义在实数上的。现在我们要问：

> **如何将这些函数扩展到复数域？**

例如，$e^{1+i}$ 是什么意思？$\sin(i)$ 等于多少？

#### 幂级数方法

最自然的方法是使用**泰勒级数**（Taylor Series）。许多实函数可以表示为幂级数：
$$f(x) = \sum_{n=0}^{\infty} a_n x^n = a_0 + a_1 x + a_2 x^2 + a_3 x^3 + \cdots$$

**核心思想**：将实变量 $x$ 替换为复变量 $z$：
$$f(z) = \sum_{n=0}^{\infty} a_n z^n$$

只要级数收敛，这就定义了复变函数。

#### 为什么幂级数方法有效？

1. **一致性**：当 $z$ 是实数时，结果与原实函数一致
2. **唯一性**：解析延拓是唯一的（后面会讲恒等定理）
3. **保持性质**：保持了微分、积分等分析性质

---

### 1.2 指数函数：$e^z$ 的定义

#### 实指数函数的泰勒级数

实指数函数 $e^x$ 的泰勒级数为：
$$e^x = \sum_{n=0}^{\infty} \frac{x^n}{n!} = 1 + x + \frac{x^2}{2!} + \frac{x^3}{3!} + \cdots$$

这个级数对所有实数 $x$ 都收敛。

#### 复指数函数的定义

将 $x$ 替换为 $z$，得到**复指数函数**：
$$e^z = \sum_{n=0}^{\infty} \frac{z^n}{n!} = 1 + z + \frac{z^2}{2!} + \frac{z^3}{3!} + \cdots$$

这个级数对**所有复数** $z$ 都收敛。

#### 指数函数的性质

复指数函数保持了实指数函数的许多性质：

| 性质 | 表达式 |
|------|--------|
| 加法公式 | $e^{z_1 + z_2} = e^{z_1} \cdot e^{z_2}$ |
| 导数 | $\frac{d}{dz}e^z = e^z$ |
| 不为零 | $e^z \neq 0$ 对所有 $z$ |

#### 与三角函数的联系：欧拉公式

将 $z = i\theta$ 代入指数级数：
$$\begin{aligned}
e^{i\theta} &= 1 + i\theta + \frac{(i\theta)^2}{2!} + \frac{(i\theta)^3}{3!} + \frac{(i\theta)^4}{4!} + \cdots \\
&= 1 + i\theta - \frac{\theta^2}{2!} - i\frac{\theta^3}{3!} + \frac{\theta^4}{4!} + i\frac{\theta^5}{5!} - \cdots \\
&= \left(1 - \frac{\theta^2}{2!} + \frac{\theta^4}{4!} - \cdots\right) + i\left(\theta - \frac{\theta^3}{3!} + \frac{\theta^5}{5!} - \cdots\right) \\
&= \cos\theta + i\sin\theta
\end{aligned}$$

这就是著名的**欧拉公式**：
$$e^{i\theta} = \cos\theta + i\sin\theta$$

#### 例子：计算 $e^{1+i}$

$$\begin{aligned}
e^{1+i} &= e^1 \cdot e^i \\
&= e \cdot (\cos 1 + i\sin 1) \\
&= e\cos 1 + ie\sin 1 \\
&\approx 2.718 \cdot 0.540 + i \cdot 2.718 \cdot 0.841 \\
&\approx 1.469 + 2.287i
\end{aligned}$$

---

### 1.3 三角函数：复数域的定义

#### 从欧拉公式出发

由欧拉公式：
$$e^{i\theta} = \cos\theta + i\sin\theta$$
$$e^{-i\theta} = \cos\theta - i\sin\theta$$

两式相加和相减：
$$\cos\theta = \frac{e^{i\theta} + e^{-i\theta}}{2}$$
$$\sin\theta = \frac{e^{i\theta} - e^{-i\theta}}{2i}$$

#### 复三角函数的定义

将 $\theta$ 替换为复数 $z$，得到**复三角函数**：

$$\boxed{\sin z = \frac{e^{iz} - e^{-iz}}{2i}}$$

$$\boxed{\cos z = \frac{e^{iz} + e^{-iz}}{2}}$$

#### 正切函数

$$\tan z = \frac{\sin z}{\cos z} = \frac{e^{iz} - e^{-iz}}{i(e^{iz} + e^{-iz})}$$

#### 例子：计算 $\sin(i)$

$$\begin{aligned}
\sin(i) &= \frac{e^{i\cdot i} - e^{-i\cdot i}}{2i} \\
&= \frac{e^{-1} - e^{1}}{2i} \\
&= \frac{1/e - e}{2i} \\
&= \frac{1/e - e}{2i} \cdot \frac{i}{i} \\
&= \frac{i(1/e - e)}{-2} \\
&= \frac{e - 1/e}{2}i \\
&\approx 1.175i
\end{aligned}$$

**注意**：$\sin(i)$ 是纯虚数！这与实数情况完全不同。

#### 复三角函数的性质

| 性质 | 说明 |
|------|------|
| 周期性 | $\sin(z + 2\pi) = \sin z$，$\cos(z + 2\pi) = \cos z$ |
| 无界性 | $|\sin z|$ 和 $|\cos z|$ 在复平面上无界 |
| 导数 | $\frac{d}{dz}\sin z = \cos z$，$\frac{d}{dz}\cos z = -\sin z$ |
| 加法公式 | 与实数情况相同 |

---

## 2. 逆运算的多值性

### 2.1 复对数：$\operatorname{Log} z$

#### 实对数的回顾

实对数 $\ln x$ 是指数函数的反函数：
$$y = \ln x \quad \Leftrightarrow \quad e^y = x$$

定义域：$x > 0$，值域：$\mathbb{R}$。

#### 复对数的定义

类似地，复对数定义为：
$$w = \operatorname{Log} z \quad \Leftrightarrow \quad e^w = z$$

#### 多值性的来源

问题在于：复指数函数是**周期函数**！
$$e^{w + 2k\pi i} = e^w \cdot e^{2k\pi i} = e^w \cdot 1 = e^w$$

所以，如果 $w$ 是 $z$ 的对数，那么 $w + 2k\pi i$ 也是！

#### 复对数的公式

设 $z = re^{i\theta}$（极坐标形式），则：
$$\boxed{\operatorname{Log} z = \ln r + i(\theta + 2k\pi), \quad k \in \mathbb{Z}}$$

其中：
- $\ln r$ 是实数自然对数（单值）
- $\theta = \arg z$ 是辐角（多值）

#### 例子：计算 $\operatorname{Log}(-1)$

$-1$ 的极坐标形式：$r = 1$，$\theta = \pi$

$$\operatorname{Log}(-1) = \ln 1 + i(\pi + 2k\pi) = i(\pi + 2k\pi)$$

当 $k = 0$ 时：$\operatorname{Log}(-1) = i\pi$
当 $k = 1$ 时：$\operatorname{Log}(-1) = 3\pi i$
...

**著名恒等式**：$e^{i\pi} + 1 = 0$

---

### 2.2 分支切割：使函数单值化

#### 主值分支

为了得到单值函数，我们选择**主值分支**（principal branch）：
$$\operatorname{log} z = \ln|z| + i\operatorname{Arg} z$$

其中 $\operatorname{Arg} z$ 是**主辐角**，取值范围为 $(-\pi, \pi]$。

#### 分支切割

主值分支在**负实轴**上不连续：
- 从上方趋近：$\operatorname{Arg} z \to \pi$
- 从下方趋近：$\operatorname{Arg} z \to -\pi$

这条不连续线称为**分支切割**（branch cut）。

#### 黎曼面的思想

为了完整处理多值性，数学家引入了**黎曼面**：
- 将复平面"切开"
- 将多个副本（叶）沿切口粘合
- 形成一个多层的曲面

在黎曼面上，多值函数变成单值函数。

---

### 2.3 黎曼面：处理多值性的拓扑工具

#### 黎曼面的直观理解

以复对数为例：
- 每一"层"对应一个 $k$ 值
- 沿分支切割从一个层走到另一个层
- 形成一个无限层的螺旋面

#### 平方根函数的黎曼面

$w = \sqrt{z}$ 有两个值（正负根），其黎曼面有两层：
- 第一层：主值分支
- 第二层：负值分支
- 绕原点一周，从一层到另一层
- 绕两周，回到原层

#### 黎曼面的意义

黎曼面是**复分析**与**拓扑学**的交汇点：
- 将多值函数转化为单值函数
- 揭示了复函数的深层几何结构
- 是现代代数几何的基础

---

## 3. 复变函数的特殊性质

### 3.1 柯西 - 黎曼方程

#### 复变函数的分解

设 $f(z)$ 是复变函数，$z = x + iy$，则：
$$f(z) = u(x, y) + iv(x, y)$$

其中 $u, v$ 是实值函数，分别表示实部和虚部。

#### 柯西 - 黎曼方程

$f(z)$ 在某点**可微**（解析）的充要条件是 $u, v$ 满足：

$$\boxed{\frac{\partial u}{\partial x} = \frac{\partial v}{\partial y}}$$

$$\boxed{\frac{\partial u}{\partial y} = -\frac{\partial v}{\partial x}}$$

#### 例子：验证 $f(z) = z^2$ 的解析性

$f(z) = z^2 = (x+iy)^2 = x^2 - y^2 + 2xyi$

所以 $u = x^2 - y^2$，$v = 2xy$。

计算偏导数：
- $\frac{\partial u}{\partial x} = 2x$，$\frac{\partial v}{\partial y} = 2x$ ✓
- $\frac{\partial u}{\partial y} = -2y$，$-\frac{\partial v}{\partial x} = -2y$ ✓

满足柯西 - 黎曼方程，所以 $f(z) = z^2$ 是解析函数。

#### 柯西 - 黎曼方程的意义

1. **解析性的判据**：判断复函数是否可微
2. **实虚部的耦合**：$u$ 和 $v$ 不是独立的
3. **调和函数**：满足 C-R 方程的 $u, v$ 都是调和函数（满足拉普拉斯方程）

---

### 3.2 保形性：解析函数保持角度

#### 保形映射的定义

**保形映射**（conformal map）是保持角度不变的映射。

#### 解析函数的保形性

**定理**：如果 $f(z)$ 在 $z_0$ 处解析且 $f'(z_0) \neq 0$，则 $f$ 在 $z_0$ 附近是保形的。

#### 几何解释

```
原平面 z：          像平面 w：
    ↑ Im               ↑ Im
    |                  |
    |  θ               |  θ (角度不变)
    | /                | /
----+/----→ Re   →   ----+/----→ Re
   /|                 /|
  / |                / |
```

两条曲线的夹角在映射前后保持不变。

#### 应用

- **流体力学**：保形映射用于求解势流问题
- **电磁学**：计算电场和磁场的分布
- **地图投影**：墨卡托投影是保形的

---

### 3.3 恒等定理：解析延拓的唯一性

#### 恒等定理的内容

> **恒等定理**：如果两个解析函数 $f$ 和 $g$ 在某个区域内的一小段（甚至一个收敛点列）上相等，则它们在整个区域上相等。

#### 直观理解

解析函数具有"刚性"：
- 知道一小部分，就能确定整体
- 不像实函数可以"局部修改"

#### 解析延拓的唯一性

**推论**：解析延拓是唯一的。

如果 $f$ 是定义在区域 $D$ 上的解析函数，那么它到更大区域 $D'$ 的解析延拓（如果存在）是唯一的。

#### 例子：$\sin z$ 的唯一性

- 实正弦函数 $\sin x$ 定义在 $\mathbb{R}$ 上
- 通过幂级数延拓到 $\mathbb{C}$：$\sin z = \sum_{n=0}^{\infty} (-1)^n \frac{z^{2n+1}}{(2n+1)!}$
- 由恒等定理，这是**唯一**的解析延拓

---

## 本章小结

### 复函数的定义

| 函数 | 定义 |
|------|------|
| 指数函数 | $e^z = \sum_{n=0}^{\infty} \frac{z^n}{n!}$ |
| 正弦函数 | $\sin z = \frac{e^{iz} - e^{-iz}}{2i}$ |
| 余弦函数 | $\cos z = \frac{e^{iz} + e^{-iz}}{2}$ |
| 复对数 | $\operatorname{Log} z = \ln|z| + i(\arg z + 2k\pi)$ |

### 核心概念

| 概念 | 说明 |
|------|------|
| 解析延拓 | 通过幂级数将实函数扩展到复数域 |
| 多值性 | 复对数等逆运算是多值的 |
| 分支切割 | 选择主值分支使函数单值化 |
| 柯西 - 黎曼方程 | $\frac{\partial u}{\partial x} = \frac{\partial v}{\partial y}$，$\frac{\partial u}{\partial y} = -\frac{\partial v}{\partial x}$ |
| 保形性 | 解析函数保持角度不变 |
| 恒等定理 | 解析延拓的唯一性 |

---

## 思考题

1. 用幂级数定义计算 $e^{i\pi}$，验证欧拉恒等式。
2. 计算 $\cos(i)$ 的值。
3. 为什么复对数是多值的？主值分支如何选择？
4. 验证 $f(z) = e^z$ 满足柯西 - 黎曼方程。

## 下一章预告

在第六章中，我们将探讨复数与矩阵之间的深刻联系。复数可以用 $2 \times 2$ 实矩阵表示，这种表示揭示了两者之间的代数同构关系。
