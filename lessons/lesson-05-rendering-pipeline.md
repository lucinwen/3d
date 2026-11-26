# 第 5 讲：Rendering Pipeline

## 1. 概念

Rendering Pipeline 将三维场景转换为二维图像。典型阶段包括对象/顶点处理、裁剪、光栅化、片元处理、深度/模板测试、混合和后处理。

## 2. 原理

典型坐标变换：
[
p_{clip}=PVMp_{local}
]
M 为 Model Matrix，V 为 View Matrix，P 为 Projection Matrix。齐次裁剪后进行透视除法，得到 NDC，再映射到屏幕坐标。

Rasterization 将三角形覆盖关系转换为片元；Depth Test 使用深度缓冲判断可见性。透明物体通常需要额外排序或 OIT 等策略。

## 3. 数据结构

- Vertex Buffer / Index Buffer。
- Uniform / Constant Buffer。
- Texture / Sampler。
- Framebuffer。
- Depth Buffer / Stencil Buffer。
- Render Target。
- Draw Call / Pipeline State。

## 4. 算法

主要步骤：
1. 顶点变换。
2. Primitive Assembly。
3. Clipping。
4. Perspective Divide。
5. Viewport Transform。
6. Rasterization。
7. Fragment Shading。
8. Depth/Stencil Test。
9. Blending。
10. Post-processing。

常见技术：
- Shadow Mapping。
- MSAA/FXAA/TAA。
- Mipmap。
- HDR 与 Tone Mapping。
- Deferred/Forward Rendering。

## 5. 工程实现

使用 Blender 或 UE 建立标准测试场景，固定相机、光照、曝光和分辨率，对同一资产输出 Beauty、Depth、Normal、Mask、Object ID 等通道。保存渲染配置以保证可复现。

## 6. 评价指标

- Render Time / GPU Frame Time。
- Frame Stability。
- Silhouette / Pixel Difference。
- Temporal Flicker。
- Shadow/Transparency Artifacts。
- Memory Usage。
视觉误差比较必须固定相机、光照、曝光和色彩管理。

## 7. 实际案例

同一角色在 Blender 正常、导入 UE 后材质发黑，可能涉及切线空间、法线贴图格式、色彩空间、材质模型或渲染设置差异。应使用标准材质球和中间通道逐项定位，而非直接修改 Mesh。

## 8. 面试追问

- Rasterization 与 Ray Tracing 有何区别？
- Depth Buffer 如何工作？
- 为什么透明物体排序困难？
- Mipmap 解决什么问题？
- 如何建立可复现的渲染评测？

## 9. 小测

画出一条典型实时渲染管线；设计一套 Blender/UE 跨引擎渲染一致性测试。
