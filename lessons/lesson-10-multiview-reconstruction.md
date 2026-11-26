# 第 10 讲：Multi-view Reconstruction

## 1. 概念

多视图重建利用同一场景在不同相机视角下的图片，恢复相机参数和三维结构。输出可包括相机位姿、稀疏/稠密点云、深度图和 Mesh。Multi-view Reconstruction 与 Multi-view Generation 不同：前者从观测恢复，后者生成视图。

## 2. 原理

### 视差
校正双目模型：
[
Z=fB/d
]
f 为像素焦距，B 为基线，d 为视差。小视差时深度对像素误差更敏感。基线太小深度不敏感，太大则共同视野减少。

### 极线几何
两相机光心和空间点形成极平面，与图像平面相交得到极线。像素齐次坐标满足：
[
p_2^TFp_1=0
]
Fundamental Matrix F 描述像素坐标关系；Essential Matrix E 描述归一化相机坐标关系：
[
E=K_2^TFK_1,quad E=[t]_	imes R
]
E 可恢复相对旋转和平移方向，但通常不能恢复绝对平移尺度。

### 三角测量
多相机观测射线相交/最小化重投影误差以估计三维点。噪声下通常求解最小二乘，线性方法可用 SVD，再进行非线性优化。

## 3. 数据结构

- Keypoint：位置、尺度、方向。
- Descriptor：局部外观向量。
- Match：两图特征对应。
- Camera：内参、外参、畸变。
- Track：同一 3D 点在多张图中的观测。
- Point3D：XYZ、颜色、误差、Track。
- Camera Graph：图片/相机节点与匹配边。

## 4. 算法

### SIFT
尺度空间、高斯差分 DoG、关键点定位、方向分配、经典 128 维梯度直方图描述子。对尺度/旋转较鲁棒，但计算较重。

### ORB
FAST 角点 + Oriented BRIEF 二进制描述子，常用 Hamming Distance，速度快但对大尺度变化通常不如 SIFT。

### 匹配与 RANSAC
KNN、Lowe Ratio Test、Cross-check 筛选候选匹配；RANSAC 随机采样估计模型并统计 Inliers。RANSAC 降低外点影响，但不能保证模型一定正确。

迭代次数近似：
[
N=rac{log(1-p)}{log(1-w^s)}
]
p 为目标成功概率，w 为内点比例，s 为最小采样数。

### SfM
Feature Detection → Matching → Geometric Verification → Camera Pose → Triangulation → Bundle Adjustment → Sparse Reconstruction。
Incremental SfM 逐步注册相机；Global SfM 利用全局相机关系估计位姿。

### Bundle Adjustment
联合优化相机参数和三维点，使观测与重投影误差最小：
[
min_{{C_i},{X_j}}sum_{(i,j)}ho(|p_{ij}-pi(C_i,X_j)|^2)
]
常用 Gauss-Newton、Levenberg-Marquardt 和稀疏优化。需处理 Gauge Freedom，固定参考相机/尺度。

### MVS
在相机位姿已知基础上进行多视图稠密深度估计、过滤、融合和表面重建。Plane Sweeping/Cost Volume 是经典思路。反光、透明、低纹理、遮挡和重复纹理是困难情况。

## 5. 工程实现

COLMAP 常见流程：
1. 准备同一静态场景的重叠图片。
2. feature_extractor。
3. sequential_matcher 或 exhaustive_matcher。
4. mapper 生成 sparse model。
5. image_undistorter。
6. patch_match_stereo。
7. stereo_fusion。
8. 后续 Mesh 重建与清理。

命令示例：
```bash
colmap feature_extractor --database_path database.db --image_path images
colmap sequential_matcher --database_path database.db
colmap mapper --database_path database.db --image_path images --output_path sparse
```
具体参数随版本、相机类型和 GPU 构建变化。检查注册图片数、相机位姿、稀疏点云、重投影误差、稠密深度和融合点云，不要只看最终 Mesh。

## 6. 评价指标

- Match Count / Inlier Ratio。
- Camera Rotation/Translation Error（需坐标和尺度对齐）。
- Reprojection Error（像素）。
- Depth MAE/RMSE。
- Chamfer Distance、F-score、Normal Consistency（需 GT）。
- Completeness/Coverage。
- Multi-view Consistency。
- Mesh Validity / Production Readiness。

低重投影误差不保证真实几何正确；高 Inlier Ratio 不保证场景深度覆盖充分。

## 7. 实际案例

室内场景重建：定义图片和相机参考→构建 Camera Graph→SfM/BA→MVS→深度融合→稠密点云/Mesh→对象级位置、几何级尺寸/形状、关系级邻接/接触/前后约束→多视角重投影验收。

## 8. 面试追问

- SIFT 与 ORB 的区别？
- RANSAC 如何识别外点？
- F 与 E 有何区别？
- 为什么单目 SfM 有尺度歧义？
- SfM 和 MVS 如何分工？
- BA 优化什么？
- 重投影误差低但空间结构错误，可能是什么原因？

## 9. 小测

解释视差公式；描述 COLMAP 全流程；设计一套区分相机位姿、深度、物体位置和语义关系错误的 Benchmark。
