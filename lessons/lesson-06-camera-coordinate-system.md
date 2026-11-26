# 第 6 讲：Camera 与 Coordinate System

## 1. 概念

Local、World、View、Clip、NDC、Screen Space 是不同参考空间。Camera Intrinsics 描述成像参数；Extrinsics 描述世界与相机之间的位姿变换。

## 2. 原理

针孔模型：
[
u=f_xX/Z+c_x,quad v=f_yY/Z+c_y
]
其中 X/Y/Z 为相机坐标，fx/fy 为像素焦距，cx/cy 为主点。世界到相机变换常写为：
[
X_c=R X_w+t
]
若相机在世界坐标中的位置为 C，则在相应约定下 (t=-RC)，所以外参平移不直接等于相机世界位置。

## 3. 数据结构

- Intrinsics K：3×3。
- Extrinsics：R、t 或 4×4 齐次矩阵。
- Distortion：径向/切向畸变参数。
- Pose：位置与旋转（矩阵、欧拉角或四元数）。
- Projection Matrix：K[R|t]。

## 4. 算法

- Camera Calibration：使用棋盘格等已知几何估计内参和畸变。
- Projection：3D 点映射至像素。
- Back-projection：深度图和内参恢复相机坐标点。
- Triangulation：多视图射线恢复 3D 点。
- Coordinate Conversion：轴向、手性、单位、矩阵约定转换。

## 5. 工程实现

OpenCV projectPoints 可计算投影；triangulatePoints 可做线性三角测量。实际工程还要进行畸变处理、正深度检查、重投影验证和坐标系对齐。Blender、UE、OpenCV 的轴向和单位约定需要显式转换，不能凭经验猜。

## 6. 评价指标

- Reprojection Error（像素）。
- Rotation Error（角度）。
- Translation Error（长度单位，需尺度对齐）。
- Depth MAE/RMSE。
- Calibration Reprojection Error。
单目重建通常存在全局尺度歧义；评价前必须固定坐标和尺度协议。

## 7. 实际案例

Blender 资产导入 UE 后旋转反向或尺寸异常，依次检查轴向映射、单位、对象变换、矩阵方向、手性、法线逆转置和三角面绕序。

## 8. 面试追问

- 为什么 View Matrix 是相机世界变换的逆？
- Intrinsics 和 Extrinsics 有什么区别？
- 为什么单张图片无法确定绝对深度？
- 四元数与欧拉角如何选择？
- 外参 t 为什么不等于相机位置？

## 9. 小测

推导针孔投影和深度反投影；给定相机内外参，计算一个点的像素位置；说明坐标系转换的测试策略。
