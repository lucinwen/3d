# 第 3 讲：Material 与 PBR

## 1. 概念

Material 描述表面如何与光交互。PBR（Physically Based Rendering）使用近似物理的光照模型和参数，使材质在不同光照环境下表现更稳定。PBR 是渲染工作流，不等于所有参数都是真实测量值。

## 2. 原理

BRDF（Bidirectional Reflectance Distribution Function）描述入射光方向与出射光方向之间的反射关系。

常见微表面模型包括 Cook-Torrance：
[
f_r = rac{DGF}{4(Ncdot L)(Ncdot V)}
]
其中 D 为法线分布项，G 为几何遮蔽项，F 为 Fresnel 项。实际渲染还要考虑漫反射、能量守恒和数值稳定。

GGX 是常见微表面法线分布模型；Fresnel 描述反射率随观察角度变化；Roughness 控制微表面粗糙程度。

## 3. 数据结构

常见 Metallic-Roughness 工作流：
- Base Color。
- Metallic。
- Roughness。
- Normal。
- Ambient Occlusion（视管线而定）。
- Emissive。
- Alpha。

贴图还需记录：
- 文件路径。
- 分辨率。
- 通道打包方式。
- 色彩空间。
- UV 集。
- 材质槽引用。

Base Color 通常按 sRGB 纹理读取；法线、粗糙度、金属度等数据贴图通常按线性数据读取。具体取决于引擎和管线。

## 4. 算法

材质渲染一般结合：
1. 读取材质参数和纹理。
2. 采样法线。
3. 计算 N、L、V、H 等向量。
4. 计算 Fresnel、法线分布和几何遮蔽。
5. 组合漫反射与镜面反射。
6. 进行曝光、色调映射和颜色输出。

## 5. 工程实现

Blender Principled BSDF 可通过节点连接 Base Color、Metallic、Roughness、Normal 等输入。法线贴图需通过 Normal Map 节点正确解释，不能直接当颜色贴图使用。

批量检查应验证节点存在、贴图路径有效、色彩空间正确、材质槽绑定完整，并进行实际渲染回归。

## 6. 评价指标

- 参数合法性：数值范围、缺失引用。
- Texture Completeness：必需贴图是否存在。
- Render Consistency：统一光照/相机下的外观一致性。
- Material Classification Accuracy：材质类别识别准确性。
仅凭 Metallic/Roughness 参数不能证明视觉材质正确。

## 7. 实际案例

金属物体看起来像塑料，可能是环境反射不足、Metallic 贴图错误、Roughness 过高、法线异常或色彩空间配置错误。应通过参数检查和标准环境渲染分开定位。

## 8. 面试追问

- BRDF 是什么？
- Cook-Torrance 的 D/G/F 分别是什么？
- Metallic-Roughness 与 Specular-Glossiness 有何区别？
- 为什么 Normal Map 不能按 sRGB 处理？
- 参数正确为什么不代表材质外观正确？

## 9. 小测

解释 BRDF、GGX、Fresnel、Roughness；设计一套材质节点自动检查与标准球渲染验收方案。
