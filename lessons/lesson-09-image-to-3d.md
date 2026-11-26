# 第 9 讲：Image-to-3D

## 1. 概念

Image-to-3D 根据二维图像恢复或生成三维表示。它属于逆向图形学问题。单张图像通常无法唯一确定完整几何；输出可能是推断结果，不一定等于物体真实原始形状。

## 2. 原理

三维线索包括 Silhouette、Shading、Occlusion、Perspective、Texture Gradient、Cast Shadow、Semantic Prior。可见几何由图像约束；不可见几何依赖先验推断，必须区分 Observed Geometry 与 Inferred Geometry。

贝叶斯直觉：
[
P(G|I)propto P(I|G)P(G)
]
既要解释输入图像，也要符合合理形状先验。

## 3. 数据结构

RGB、Mask、Depth、Normal、Camera Intrinsics/Extrinsics、Point Cloud、Mesh、Texture、Latent。Depth 必须声明 Metric/Relative/Inverse/Normalized 类型、单位和无效值约定。

## 4. 算法

### 深度反投影
[
X=(u-c_x)Z/f_x,quad Y=(v-c_y)Z/f_y,quad Z=D(u,v)
]
得到相机坐标系点云。再通过外参变换到世界坐标。

### 深度估计
- Monocular：单图预测，依赖先验，绝对尺度可能不确定。
- Stereo：双目视差，校正相机下 (Z=fB/d)。
- Multi-view：利用多个视角共同约束深度。

### Point Cloud 到 Mesh
- Poisson：利用有向点云构建隐式表面，可能过度平滑或补出不存在表面。
- Ball Pivoting：滚球连接邻近点，对密度和半径敏感。
- Delaunay：需结合表面约束，不能直接把三维点三角化就视为正确表面。

### 其他路线
- Multi-view Generation：先生成新视角，再重建；生成视图不保证几何一致。
- Direct 3D Generation：Image Encoder → 3D Latent/Decoder。
- Optimization-based：渲染与输入比较，优化三维参数。

## 5. 工程实现

可用 OpenCV/Numpy 对 Metric Depth 反投影，Open3D 生成点云、滤波、估计法线和尝试 Poisson 重建。必须明确深度单位、相机内参、图像裁剪缩放、坐标系和深度边界；单图可见点云不能自动补全真实背面。

## 6. 评价指标

- Silhouette IoU。
- Depth MAE/RMSE/AbsRel。
- Chamfer Distance、F-score、Normal Consistency（需要三维 GT）。
- Reprojection Error。
- Multi-view Consistency。
- Completeness。
- Asset Usability。
无 GT 时使用结构规则、专家评审和明确标注的代理指标，不虚构几何误差。

## 7. 实际案例

二次元角色单图生成：解析部件和属性→分割/深度/相机→三维生成或多视角生成→检查视图一致性→几何提取→拓扑/UV/材质→Rig/UE 验收。复杂头发、遮挡、非对称和细长结构应作为困难样本。

## 8. 面试追问

- 单张图片为什么不能唯一恢复三维？
- Depth Map 如何反投影？
- Shape Prior 有何价值和风险？
- Point Cloud 与 Mesh 有何区别？
- 为什么多视角生成不等于多视角一致？
- 没有 GT Mesh 怎样评价？

## 9. 小测

推导反投影；比较深度式、直接生成式和优化式路线；设计单图角色重建失败诊断。
