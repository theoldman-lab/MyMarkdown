# 第六章：复数与矩阵的关系

## 1. 复数的矩阵表示

### 1.1 同构映射：从复数到矩阵

#### 核心对应关系

每个复数 $z = a + bi$ 可以对应一个 $2 \times 2$ 实矩阵：

$$\boxed{a + bi \quad \longleftrightarrow \quad \begin{pmatrix} a & -b \\ b & a \end{pmatrix}}$$

#### 为什么是这种形式？

让我们从几何角度理解。复数 $z = a + bi$ 可以看作平面上的变换：
- 将点 $(x, y)$ 映射到 $(ax - by, bx + ay)$

这正是矩阵 $\begin{pmatrix} a & -b \\ b & a \end{pmatrix}$ 的作用：
$$\begin{pmatrix} a & -b \\ b & a \end{pmatrix} \begin{pmatrix} x \\ y \end{pmatrix} = \begin{pmatrix} ax - by \\ bx + ay \end{pmatrix}$$

#### 特殊复数的矩阵表示

| 复数 | 矩阵 |
|------|------|
| $1 = 1 + 0i$ | $\begin{pmatrix} 1 & 0 \\ 0 & 1 \end{pmatrix} = I$ |
| $i = 0 + 1i$ | $\begin{pmatrix} 0 & -1 \\ 1 & 0 \end{pmatrix} = J$ |
| $0 = 0 + 0i$ | $\begin{pmatrix} 0 & 0 \\ 0 & 0 \end{pmatrix}$ |
| $-1 = -1 + 0i$ | $\begin{pmatrix} -1 & 0 \\ 0 & -1 \end{pmatrix} = -I$ |

---

### 1.2 结构验证：运算的保持

#### 加法对应

设 $z_1 = a + bi$，$z_2 = c + di$，对应矩阵：
$$M_1 = \begin{pmatrix} a & -b \\ b & a \end{pmatrix}, \quad M_2 = \begin{pmatrix} c & -d \\ d & c \end{pmatrix}$$

复数加法：
$$z_1 + z_2 = (a+c) + (b+d)i$$

矩阵加法：
$$M_1 + M_2 = \begin{pmatrix} a+c & -b-d \\ b+d & a+c \end{pmatrix}$$

**结论**：加法运算完全对应！

#### 乘法对应

复数乘法：
$$z_1 \cdot z_2 = (a+bi)(c+di) = (ac-bd) + (ad+bc)i$$

矩阵乘法：
$$\begin{aligned}
M_1 M_2 &= \begin{pmatrix} a & -b \\ b & a \end{pmatrix} \begin{pmatrix} c & -d \\ d & c \end{pmatrix} \\
&= \begin{pmatrix} ac-bd & -ad-bc \\ bc+ad & -bd+ac \end{pmatrix} \\
&= \begin{pmatrix} ac-bd & -(ad+bc) \\ ad+bc & ac-bd \end{pmatrix}
\end{aligned}$$

这正是 $(ac-bd) + (ad+bc)i$ 对应的矩阵！

#### 验证 $i^2 = -1$

复数：$i^2 = -1$

矩阵：
$$J^2 = \begin{pmatrix} 0 & -1 \\ 1 & 0 \end{pmatrix}^2 = \begin{pmatrix} 0 & -1 \\ 1 & 0 \end{pmatrix} \begin{pmatrix} 0 & -1 \\ 1 & 0 \end{pmatrix} = \begin{pmatrix} -1 & 0 \\ 0 & -1 \end{pmatrix} = -I$$

**完美对应**！

---

### 1.3 几何诠释：旋转缩放矩阵

#### 复数的极坐标形式

复数 $z = a + bi$ 可以写成极坐标形式：
$$z = r(\cos\theta + i\sin\theta) = re^{i\theta}$$

其中 $r = \sqrt{a^2 + b^2}$，$\theta = \arg(z)$。

#### 对应的矩阵形式

将 $a = r\cos\theta$，$b = r\sin\theta$ 代入矩阵：
$$\begin{aligned}
M_z &= \begin{pmatrix} r\cos\theta & -r\sin\theta \\ r\sin\theta & r\cos\theta \end{pmatrix} \\
&= r \begin{pmatrix} \cos\theta & -\sin\theta \\ \sin\theta & \cos\theta \end{pmatrix}
\end{aligned}$$

这正是**旋转缩放矩阵**！

#### 分解理解

$$r \begin{pmatrix} \cos\theta & -\sin\theta \\ \sin\theta & \cos\theta \end{pmatrix} = \underbrace{\begin{pmatrix} r & 0 \\ 0 & r \end{pmatrix}}_{\text{缩放}} \cdot \underbrace{\begin{pmatrix} \cos\theta & -\sin\theta \\ \sin\theta & \cos\theta \end{pmatrix}}_{\text{旋转}}$$

- **缩放**：将向量长度放大 $r$ 倍
- **旋转**：逆时针旋转 $\theta$ 角度

#### 例子：$1+i$ 的几何意义

$1+i = \sqrt{2} e^{i\pi/4}$

对应矩阵：
$$\begin{aligned}
M_{1+i} &= \begin{pmatrix} 1 & -1 \\ 1 & 1 \end{pmatrix} \\
&= \sqrt{2} \begin{pmatrix} \cos(\pi/4) & -\sin(\pi/4) \\ \sin(\pi/4) & \cos(\pi/4) \end{pmatrix} \\
&= \sqrt{2} \begin{pmatrix} \frac{\sqrt{2}}{2} & -\frac{\sqrt{2}}{2} \\ \frac{\sqrt{2}}{2} & \frac{\sqrt{2}}{2} \end{pmatrix}
\end{aligned}$$

几何意义：旋转 $45°$ 并放大 $\sqrt{2}$ 倍。

---

## 2. 复数与矩阵的异同

### 2.1 相似之处

#### 运算一致性

在复数矩阵表示的子代数内，运算完全一致：

| 运算 | 复数 | 矩阵 |
|------|------|------|
| 加法 | $z_1 + z_2$ | $M_1 + M_2$ |
| 乘法 | $z_1 \cdot z_2$ | $M_1 M_2$ |
| 逆 | $z^{-1}$ | $M^{-1}$ |
| 共轭 | $\bar{z}$ | $M^T$（转置） |

#### 特征值联系

复数 $z = a + bi$ 对应矩阵 $M = \begin{pmatrix} a & -b \\ b & a \end{pmatrix}$ 的特征值为：
$$\lambda = a \pm bi = z, \bar{z}$$

**推导**：
$$\det(M - \lambda I) = \det\begin{pmatrix} a-\lambda & -b \\ b & a-\lambda \end{pmatrix} = (a-\lambda)^2 + b^2 = 0$$
$$(a-\lambda)^2 = -b^2 \Rightarrow a-\lambda = \pm bi \Rightarrow \lambda = a \pm bi$$

#### 指数函数定义一致

复数指数：$e^z = \sum_{n=0}^{\infty} \frac{z^n}{n!}$

矩阵指数：$e^M = \sum_{n=0}^{\infty} \frac{M^n}{n!}$

如果 $M$ 是复数 $z$ 的矩阵表示，则 $e^M$ 是 $e^z$ 的矩阵表示。

---

### 2.2 相异之处

#### 交换律的差异

**复数**：乘法满足交换律
$$z_1 z_2 = z_2 z_1$$

**矩阵**：乘法一般不满足交换律
$$AB \neq BA \quad \text{（一般情况下）}$$

**特例**：复数对应的矩阵形式 $\begin{pmatrix} a & -b \\ b & a \end{pmatrix}$ 之间是可交换的，但一般矩阵不可交换。

#### 代数结构的差异

| 结构 | 复数 $\mathbb{C}$ | 矩阵 $M_n(\mathbb{R})$ |
|------|------------------|----------------------|
| 类型 | **域**（Field） | **环**（Ring） |
| 可除性 | 每个非零元有逆 | 存在零因子，不可逆矩阵 |
| 交换律 | 满足 | 不满足 |
| 维度 | 2 维（ over $\mathbb{R}$） | $n^2$ 维 |

#### 零因子的存在

**复数**：没有零因子
$$z_1 z_2 = 0 \Rightarrow z_1 = 0 \text{ 或 } z_2 = 0$$

**矩阵**：存在零因子
$$\begin{pmatrix} 1 & 0 \\ 0 & 0 \end{pmatrix} \begin{pmatrix} 0 & 0 \\ 0 & 1 \end{pmatrix} = \begin{pmatrix} 0 & 0 \\ 0 & 0 \end{pmatrix}$$

两个非零矩阵相乘可以得到零矩阵！

#### 通用性的差异

**复数**：只能表示二维平面上的旋转和缩放

**矩阵**：可以表示
- 任意维度的线性变换
- 剪切变换
- 投影变换
- 更复杂的操作

---

## 深入理解：为什么复数矩阵是这种形式？

### 从线性变换角度

考虑复数乘法 $z \cdot w$，其中 $z = a + bi$ 固定，$w = x + yi$ 是变量。

$$z \cdot w = (a+bi)(x+yi) = (ax-by) + (bx+ay)i$$

这可以看作从 $(x, y)$ 到 $(ax-by, bx+ay)$ 的线性变换：
$$\begin{pmatrix} x \\ y \end{pmatrix} \mapsto \begin{pmatrix} ax-by \\ bx+ay \end{pmatrix} = \begin{pmatrix} a & -b \\ b & a \end{pmatrix} \begin{pmatrix} x \\ y \end{pmatrix}$$

### 从基向量角度

复数平面的基是 $\{1, i\}$。

复数 $z = a + bi$ 的作用：
- $z \cdot 1 = a + bi$，对应向量 $(a, b)$
- $z \cdot i = -b + ai$，对应向量 $(-b, a)$

矩阵的列就是基向量的像：
$$M_z = \begin{pmatrix} a & -b \\ b & a \end{pmatrix}$$

第一列是 $z \cdot 1$ 的坐标，第二列是 $z \cdot i$ 的坐标。

---

## 本章小结

### 复数 - 矩阵对应

| 复数 | 矩阵 |
|------|------|
| $a + bi$ | $\begin{pmatrix} a & -b \\ b & a \end{pmatrix}$ |
| $i$ | $\begin{pmatrix} 0 & -1 \\ 1 & 0 \end{pmatrix}$ |
| $re^{i\theta}$ | $r\begin{pmatrix} \cos\theta & -\sin\theta \\ \sin\theta & \cos\theta \end{pmatrix}$ |

### 相似与相异

| 方面 | 相似 | 相异 |
|------|------|------|
| 运算 | 加法、乘法对应 | 矩阵一般不可交换 |
| 结构 | 都有单位元、逆元 | 复数是域，矩阵是环 |
| 几何 | 都表示旋转缩放 | 矩阵可表示更复杂变换 |
| 特征值 | $\lambda = a \pm bi$ | 矩阵可有重特征值 |

### 关键公式

1. **对应关系**：$a+bi \leftrightarrow \begin{pmatrix} a & -b \\ b & a \end{pmatrix}$
2. **旋转矩阵**：$R_\theta = \begin{pmatrix} \cos\theta & -\sin\theta \\ \sin\theta & \cos\theta \end{pmatrix}$
3. **特征值**：$\lambda = a \pm bi$

---

## 思考题

1. 验证 $(1+i)(1-i) = 2$ 的矩阵表示也成立。
2. 为什么复数矩阵 $\begin{pmatrix} a & -b \\ b & a \end{pmatrix}$ 之间可交换，但一般矩阵不可交换？
3. 求复数 $3+4i$ 对应矩阵的特征值。
4. 解释为什么矩阵可以表示剪切变换而复数不能。

## 下一章预告

在第七章中，我们将深入探讨矩阵的本质。矩阵究竟是什么？是数？是变换？还是数据的容器？我们将从多个视角理解这个线性代数的核心概念。
