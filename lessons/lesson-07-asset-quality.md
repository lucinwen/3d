# 第 7 讲：3D Asset 综合质量评测

## 1. 概念

3D Model 不等于完整 3D Asset。Asset 可能包含 Mesh、UV、Textures、Materials、Skeleton、Skinning、Morph Targets、Animations、Physics、Metadata 和导出配置。质量必须根据用途定义。

## 2. 原理

建议分层检查：
1. 文件与资源完整性。
2. Geometry 与 Topology。
3. UV 与 Texture。
4. Material 与 Shader。
5. Rigging 与 Animation。
6. Rendering 与视觉质量。
7. Production Readiness。

区分 Hard Gate 与 Soft Metrics。硬性门槛（如文件解析、必需骨骼、引擎导入）不能被其他维度高分抵消；软性指标可按任务权重综合评分。

## 3. 数据结构

Asset Specification、Metadata、Version、Dependency Graph、Validation Report。记录资产 ID、父版本、工具/模型版本、文件 Hash、指标、失败类型和人工复核结论。

## 4. 算法

- Geometry：退化面、非流形、边界、自相交、几何偏差。
- UV：缺失、拉伸、重叠、Texel Density、Padding。
- Material：节点引用、贴图路径、色彩空间、参数和标准渲染。
- Rig：骨骼层级、权重归一化、指定骨骼。
- Animation：标准动作下的变形、穿插、塌陷。
- Engine：导入、资源引用、运行时渲染和性能。
- Regression：修改后重新执行受影响的检查。

## 5. 工程实现

使用 Blender Python/bmesh 检查基础几何、拓扑、UV、材质和骨骼；使用引擎自动化测试完成导入和运行验收。模块化 Checker 输出统一 JSON 报告。示例检测脚本只能证明已检查的项目，不能把未实现的自相交、动画质量等写成通过。

## 6. 评价指标

按用途配置：
- 静态展示：几何、UV、材质、渲染。
- 游戏角色：额外检查骨骼、权重、动画、物理、性能。
- 3D 打印：Watertightness、Wall Thickness、Volume 等。
Benchmark 需报告各维度和生产通过率，不应只给单一总分。

## 7. 实际案例

角色裙摆动态穿插可以用固定动作序列统计相交帧/相交区域，并记录优化前后结果。历史项目示例中，80 帧测试的相关相交帧统计均值由 517.8 降至 201.4（约下降 61%）；面试时必须准确解释统计口径，不称其为通用碰撞率。

## 8. 面试追问

- 为什么 Asset 质量与 Mesh 质量不同？
- Hard Gate 和 Weighted Score 如何结合？
- Chamfer Distance 为什么不能代表生产可用性？
- 如何防止 Benchmark 数据泄漏？
- 如何建立失败分类到模型迭代的闭环？

## 9. 小测

设计一个可动画角色 Asset Specification、质量门禁、失败分类表和回归测试流程。说明哪些检查可以自动化，哪些必须人工复核。
