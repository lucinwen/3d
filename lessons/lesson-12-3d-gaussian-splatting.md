# 第 12 讲：3D Gaussian Splatting（3DGS）

> 课程 2：3D 生成模型与重建。教学稿已归档；学习者尚未完成测验和实践验收。
> 原始论文：Kerbl et al., 3D Gaussian Splatting for Real-Time Radiance Field Rendering, SIGGRAPH 2023 / ACM TOG 42(4), DOI: 10.1145/3592433.
> 论文：https://arxiv.org/abs/2308.04079
> 官方项目：https://repo-sam.inria.fr/fungraph/3d-gaussian-splatting/
> 参考实现：https://github.com/graphdeco-inria/gaussian-splatting

## 1. 概念

3DGS 使用大量显式、各向异性的三维高斯基元表示静态场景，并通过投影、屏幕空间 Splatting、可见性排序和 Alpha Compositing 实现新视角合成。其目标是高质量且高效率的 Novel View Synthesis，不等于生成标准、可编辑、可绑定的游戏 Mesh。

与 NeRF 的区别：
- NeRF：连续神经场，沿相机射线采样，查询网络预测密度和颜色，再做体渲染。
- 3DGS：显式高斯基元，投影到屏幕空间后进行 Splatting 和 Alpha 混合。
- 两者都可由多视图图像和相机位姿监督优化。
- 图像渲染质量不等于几何真实性或生产资产质量。

## 2. 原理

### 2.1 三维高斯

未归一化空间响应：
[
G(x)=\exp\left(-\frac12(x-\mu)^T\Sigma^{-1}(x-\mu)\right)
]
其中 μ 是三维中心，Σ 是 3×3 对称半正定协方差矩阵。它描述基元的空间尺度、形状和主轴方向。

各向同性高斯各方向尺度相同；各向异性高斯允许不同主轴具有不同尺度，更适合表达墙面、桌面和细长结构。

### 2.2 协方差参数化

原始 3DGS 使用尺度矩阵 S 和旋转矩阵 R：
[
\Sigma=RSS^TR^T
]
S 为对角尺度矩阵，R 由归一化四元数表示。该分解便于优化尺度和旋转，并保持协方差合法结构。

### 2.3 外观与球谐函数

颜色随观察方向变化，可使用球谐函数表示：
[
c(d)=\sum_{l=0}^{L}\sum_{m=-l}^{l}a_{lm}Y_{lm}(d)
]
Y 为球谐基函数，a 为可学习系数。原始实现常用最高阶数 3，即每个颜色通道 16 个系数，RGB 合计 48 个 SH 系数。实际存储布局以代码版本为准。

### 2.4 投影到屏幕空间

将世界坐标协方差变换到相机坐标，再用透视投影在高斯中心处的 Jacobian J 做局部线性化。若 W 表示世界到相机的线性变换部分：
[
\Sigma_{2D}=JW\Sigma W^TJ^T
]
这是一种局部近似，不是有限大小椭球透视投影的精确全局结果。二维协方差定义屏幕上的椭圆足迹。实现中通常加入小的低通滤波项，避免退化的亚像素 Splat。

### 2.5 Splatting 与 Alpha Compositing

二维高斯在像素 p 的响应可简化写成：
[
\alpha_i(p)=\alpha_{0,i}G_i(p)
]
前到后混合：
[
C=\sum_i T_i\alpha_iC_i+T_{N+1}C_{bg}
]
[
T_i=\prod_{j<i}(1-\alpha_j)
]
顺序会影响结果。高斯是空间延展且半透明的基元，实际排序是高效可见性近似，不是对所有相交体积的精确全局可见性求解。

### 2.6 Tile-based Rasterization

屏幕划分为 Tiles。将每个投影高斯分配到它覆盖的 Tiles，按 Tile 和深度组织关联项，再由 GPU 并行处理各 Tile 中相关的 Splat，避免每个高斯遍历整张屏幕。

## 3. 数据结构

一个 Gaussian Primitive 通常包含：
- Position：3 个数。
- Scale：3 个数。
- Rotation：归一化四元数，4 个数。
- Opacity：通常由未激活参数经 Sigmoid 映射。
- SH Coefficients：视角相关颜色系数。

还需要相机内外参、训练图像、优化器状态、渲染缓冲区和训练配置。

内存估算示例：若 degree-3 SH 使用 48 个 float32 系数，加上 Position 3、Scale 3、Rotation 4、Opacity 1，共 59 个 float32，即每个高斯这些属性约 236 Bytes。100 万个高斯约 236 MB；这不包括梯度、优化器状态、对齐、渲染缓冲区和其他元数据。

## 4. 算法

### 4.1 初始化
1. 采集同一静态场景的多视图图片。
2. 使用 COLMAP/SfM 估计相机位姿和稀疏点云。
3. 用稀疏点初始化 Gaussian Means。
4. 初始化尺度、旋转、不透明度和 SH。
5. 通过可微渲染优化场景。

### 4.2 优化流程
1. 选择训练相机。
2. 将高斯投影到屏幕。
3. 计算二维协方差和屏幕足迹。
4. 将高斯分配到 Tiles。
5. 按深度组织和排序。
6. 光栅化并进行 Alpha Compositing。
7. 将预测图像与真实图像比较。
8. 反向传播更新 Gaussian 参数。
9. 按训练计划执行 Density Control。

### 4.3 Adaptive Density Control
- Clone：在需要更多表示能力的局部增加相似基元。
- Split：把较大的基元拆成多个较小基元。
- Prune：删除低不透明度或满足其他低贡献条件的基元。

高斯数量并非越多越好；密度控制需要平衡视觉质量、模型规模和渲染成本。

## 5. 工程实现

官方参考实现：https://github.com/graphdeco-inria/gaussian-splatting

建议阅读顺序：
1. Gaussian model：参数存储、激活、初始化、优化和密度控制。
2. Training loop：相机采样、损失和优化调度。
3. Renderer：相机和张量如何传给渲染器。
4. CUDA Rasterizer：投影、排序、Tile 光栅化和反向传播。
5. Dataset reader：COLMAP 数据读取。

文件路径可能随版本变化。先运行小型静态场景，再研究和修改 CUDA。二维 Gaussian 绘图或 Alpha 混合示例只是教学练习，不是完整 3DGS 实现。

排障顺序：检查图片静态性与覆盖、COLMAP 注册和位姿、坐标约定、初始化点云、渲染与排序、损失和优化、密度控制。不要在相机位姿错误时盲目增加高斯数量。

## 6. 评价指标

图像质量：
- PSNR：像素误差的对数指标，通常越高越好。
- SSIM：结构相似性，通常越高越好。
- LPIPS：深度特征感知距离，通常越低越好。

性能与资源：
- FPS、Frame Time（平均/P95/P99）。
- 训练时间、渲染延迟。
- GPU 显存、Gaussian Count、模型文件大小。

几何与生产：
- 有有效 GT 几何时，提取并对齐表面后可测 Chamfer Distance、F-score、Normal Consistency、Accuracy、Completeness。
- 无 GT 几何时，不得声称得到真实 CD/F-score；可用多视图深度一致性、漂浮基元检查、语义关系和专家复核等代理检查，并明确其性质。
- 高 PSNR 不证明几何真实、拓扑合格或可进入游戏生产。

FPS 比较必须注明 GPU、分辨率、高斯数量、SH 阶数、渲染器版本和计时协议。

## 7. 实际案例

静态校园建筑重建：
1. 采集重叠多视图图片。
2. COLMAP 得到相机和稀疏点云。
3. 初始化 Gaussian 集合。
4. 训练并进行密度控制。
5. 使用留出视角测试。
6. 记录 PSNR/SSIM/LPIPS、FPS、帧时间、显存、高斯数量和文件大小。
7. 若要进入游戏生产，另行进行表面提取、Mesh 清理、Retopology、UV、碰撞和引擎验收。

## 8. 面试追问

1. 3DGS 是什么，解决什么问题？
2. 为什么使用各向异性高斯？
3. 协方差矩阵编码什么？
4. 为什么用 Scale + Rotation 参数化协方差？
5. 为什么用四元数？
6. SH 系数有什么作用？
7. 推导三维协方差投影到二维的公式。
8. 什么是 Splatting 和 Alpha Compositing？
9. 为什么 Tile-based Rasterization 高效？
10. Clone、Split、Prune 有什么区别？
11. NeRF 与 3DGS 有什么区别？
12. 为什么高质量新视角不代表游戏 Mesh 合格？
13. 怎样联合评价视觉质量、延迟、显存和生产可用性？

## 9. 小测

基础题：
1. Gaussian Primitive 包含哪些参数？
2. Covariance 控制什么？
3. 为什么用 Scale + Rotation？
4. SH 表示什么？
5. Jacobian 在投影中做什么？
6. 什么是屏幕空间 Splat？
7. 为什么需要排序和 Alpha 混合？
8. 为什么使用 Tile Rasterization？
9. Clone 与 Split 的区别？
10. 为什么 PSNR 不是几何指标？

开放题：
1. 推导各向异性三维高斯到二维屏幕椭圆的协方差投影，并解释 Jacobian。
2. 一个场景渲染良好但有 500 万个高斯、显存超预算，提出优化方案和回归 Benchmark。
3. 设计从多视图采集、SfM 初始化、3DGS 训练、质量评测到可能的游戏资产转换流程，并定义质量门禁。

评分：概念 20%，数学推导 25%，算法流程 20%，工程诊断 20%，评价与生产边界 15%。完成测验和实践后才能标记 mastered。
