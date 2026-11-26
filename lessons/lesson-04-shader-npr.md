# 第 4 讲：Shader 与 NPR

## 1. 概念

Shader 是在 GPU 渲染管线特定阶段执行的程序，用于计算顶点变换、片元颜色、材质响应或其他图形效果。NPR（Non-Photorealistic Rendering）指非写实渲染，目标是艺术化表达，不追求严格物理真实。

## 2. 原理

典型可编程渲染管线涉及 Vertex Shader、Rasterization、Fragment/Pixel Shader，现代管线还可能包含 Geometry、Tessellation、Compute 等阶段。顶点着色器处理顶点属性和变换；片元着色器计算片元颜色、光照和材质。

Toon Shading 常将连续光照映射到离散色阶；描边可通过背面膨胀、屏幕空间边缘检测或几何轮廓方法实现。

## 3. 数据结构

Shader 输入常包含：
- Position、Normal、Tangent。
- UV、Vertex Color。
- World/View/Clip Position。
- Material Uniforms。
- Texture Samplers。
- Light/Camera Parameters。

坐标空间必须明确；法线变换通常需要法线矩阵，非均匀缩放下不能简单使用 Model Matrix。

## 4. 算法

Toon Shading 示例：
[
NdotL=max(0,Ncdot L)
]
再将 NdotL 映射到若干明暗区间，例如阴影、过渡、亮部。真实实现还要处理阴影、环境光、轮廓、材质分区和时间稳定性。

PBR→NPR 不应简单把 PBR 图片交给图像模型任意重绘。若需要保留几何对应，可固定 Mesh、Camera、Depth、Normal、Object ID/Mask，仅调整材质和风格化外观，并验证轮廓与关键点。

## 5. 工程实现

在 Blender 中可用 Shader Editor 节点搭建 Toon 风格；在 UE 中可用 Material Editor/HLSL 自定义节点实现。工程检查应包括目标引擎兼容性、透明排序、描边稳定性、移动端成本和多视角表现。

## 6. 评价指标

- Style Alignment：风格是否符合参考。
- Silhouette Preservation：轮廓保持程度。
- Region/Part Consistency：部件颜色与分区。
- Temporal Stability：动画时是否闪烁。
- Performance：Shader 指令、纹理采样和 GPU 时间。
风格评分不能替代几何对应验证。

## 7. 实际案例

混元训练数据需要从 PBR 渲染图构造 NPR 风格数据，同时保持与原 Mesh 的几何对应。可采用同一 Mesh 和相机渲染辅助通道，再进行受控风格转换；之后比较轮廓、深度、法线、分割区域和关键点，低置信度样本进入人工复核。

## 8. 面试追问

- Vertex Shader 与 Fragment Shader 分别做什么？
- Toon Shading 如何实现？
- 为什么图像风格迁移可能破坏几何对应？
- 如何在保持几何不变的情况下改变外观？
- 如何评价 NPR 转换是否适合训练数据？

## 9. 小测

设计一个 PBR→NPR 数据生成流程，列出固定条件、可变条件、几何一致性检查和失败样本拒收规则。
