# 第十六讲：Retopology（自动重拓扑与生产级网格优化）

> 课程 2：3D 生成模型与重建。教学归档；测验和实践尚未验收。

## 学习目标
理解 Retopology、High/Low-poly、Edge Flow、Half-edge、QEM、Edge Collapse、Quad Remeshing、Instant Meshes、QuadriFlow、Shrinkwrap、High-to-Low Baking、Normal Map、Rigging/Skinning、Pose Validation、Benchmark，以及 AI Agent 自动化生产。

## 1. 概念

### Geometry 与 Topology
Geometry 描述顶点位置和曲面形态；Topology 描述顶点、边、面如何连接。Mesh 可表示为 M=(V,E,F)。

### Retopology
在尽量保持原始几何形状的前提下，重新构建更适合目标用途的网格连接结构。重拓扑后 Geometry(M_new)≈Geometry(M_source)，但 Topology(M_new) 与 Topology(M_source) 不同。

### Retopology vs Mesh Simplification
- Mesh Simplification 主要减少顶点和面片，尽量保持几何外观，不保证重新设计边流。
- Retopology 更关注拓扑结构、边流、面片分布和目标生产用途。
两者可组合但不可互相替代。

### High-poly / Low-poly
没有绝对统一的面数阈值，取决于平台、镜头、角色重要性、同屏数量、动画和性能预算。

### 角色为何需要 Deformation-aware Topology
角色会眨眼、张嘴、转头、弯肘、弯膝、行走和奔跑。合理拓扑有助于变形，但不能保证动画自动正确。

## 2. 网格基础概念

- Vertex：位置 (x,y,z)，还可能关联法线、UV、颜色、权重等属性。
- Edge：连接两个顶点。
- Face：由边和顶点围成，常见 Triangle、Quad、N-gon。
- Edge Loop：连续边循环。
- Edge Flow：边整体沿着几何结构、曲率和变形方向的组织方式。
- Pole：顶点连接边数与规则网格不同的位置。
- Valence：顶点连接边数。规则 Quad Mesh 的普通内部顶点通常 valence 4；边界顶点可以不同。内部 valence 3 或 5 常是非常规顶点，不必然错误。
- Curvature：平均曲率 H=(k1+k2)/2，高斯曲率 K=k1*k2。高曲率和特征变化区域通常需要更多几何表达。

## 3. 数据结构

### Adjacency
邻接关系记录顶点、边、面的邻居，支持局部拓扑操作。

### Half-edge
将无向边拆成两个相反方向的有向半边。典型字段：
- Origin：起点
- Twin：对向半边
- Next / Prev：当前面环上的下一条/上一条半边
- Face：所属面
Half-edge 有助于邻接遍历、Edge Collapse 和局部拓扑更新。它是常见网格数据结构之一，不代表 Blender 唯一的底层表示。

### Boundary
Boundary Edge 通常只被一个面使用。需要保留开放曲面边界、眼口结构、衣物开口和 UV Seam 等，不能随意跨越或塌陷。

### UV 与拓扑
UV 将三维表面映射到二维纹理空间。拓扑变化后，旧顶点索引和 UV 对应通常不再一一匹配，需重新展开或通过表面对应关系烘焙纹理。

## 4. 核心算法

### Edge Collapse
将边 e=(v1,v2) 合并为新顶点 v_new，并更新或删除相关面片，减少顶点、边和面。关键是选择候选边和新顶点位置。

### QEM（Quadric Error Metrics）
Garland & Heckbert 1997 的经典网格简化方法。对平面 ax+by+cz+d=0，令 p=(a,b,c,d)^T、x=(x,y,z,1)^T，若平面法线归一化：
[
E(x)=(p^Tx)^2=x^T(pp^T)x
]
定义 K_p=pp^T。顶点周围相邻面的误差矩阵累积：
[
Q_v=\sum_i K_i
]
Edge Collapse v1,v2→v_new 时：
[
Q_{new}=Q_{v1}+Q_{v2}
]
候选新位置 x 的误差：
[
E(x)=x^TQ_{new}x
]
算法选择误差较低的操作迭代简化。QEM 主要关注几何近似，不天然保证动画边流、UV、非流形修复或生产拓扑。

### Remeshing
重新离散化表面，可调整顶点分布、面片大小、三角形质量、四边形占比和特征对齐。Remeshing 与 Retopology 有重叠，但 Retopology 更强调目标用途和生产结构。

### Isotropic / Anisotropic Remeshing
- Isotropic：边长和面片形状尽量均匀。
- Anisotropic：允许沿特定方向拉伸网格，以适应细长结构、特征边和曲面方向。
各向同性不保证角色动画 Edge Flow 正确。

### Instant Meshes
Jakob et al., SIGGRAPH Asia 2015。使用方向场（orientation field）和位置场（position field）引导边方向与顶点位置，生成 isotropic 或 quad-dominant 网格，可处理点云、扫描和三角网格。自动结果仍不保证符合所有角色动画需求。

### QuadriFlow
Huang et al., 2018。建立在 Instant Meshes 思路上，重点减少位置场奇异性，以改善四边形网格规则性。论文使用全局最小费用网络流等约束机制。奇异点不一定能完全消除；目标是减少不利奇异性。QuadriFlow 是自动 Quad Remeshing，不等于角色动画拓扑设计。

### Feature Detection 与尺寸场
自动系统可检测几何特征（Curvature、Normal Variation、Sharp Edges、Boundary）、语义特征（部件分割、关键点、语义区域）和动画特征（关节、运动方向、变形强度）。

可定义局部网格尺寸场 h(x)，例如教学示意：
[
h(x)=\frac{h_0}{1+\lambda C(x)}
]
其中 C(x) 是归一化特征强度。实际系统应融合曲率、语义重要性和变形需求。

### Guided Retopology
用户可指定边流方向、重要轮廓、关节区域、面数预算、边界约束和对称性。几何本身无法唯一决定最佳拓扑；同一形状用于静态展示、游戏动画、面部动画或 VR 时要求不同。

## 5. High-to-Low Baking

### Baking
将高模信息投射并记录到低模纹理或属性中，常见包括 Normal、AO、Curvature、Base Color、Roughness、Metallic。

### Normal Map
通过纹理 RGB 编码法线方向，改变着色时的光照法线，不会真正改变低模几何轮廓，不能替代影响轮廓的大型几何。

### Baking Cage
低模外侧的投射笼形网格，射线从 Cage 发射到高模表面，读取对应属性并写入低模 UV 纹理。Cage 不当可能导致错误投射、黑块和部件串扰。

### Tangent Space 与 Object Space Normal
- Tangent Space：在局部切线基中表达法线，常用于动态游戏角色。
- Object Space：在物体局部坐标中表达法线，适用于特定静态资产等工作流。
UV Seam、Tangent Basis、Padding 和法线设置不一致会导致接缝伪影。

## 6. Rigging、Skinning 与动画

Rigging 建立骨骼层级，如 Root→Pelvis→Spine→Neck→Head。

Linear Blend Skinning：
[
v'=\sum_{i=1}^{K}w_iT_iv
]
v 是原始顶点，T_i 是骨骼变换，w_i 是权重，通常要求权重和为 1。拓扑影响顶点密度、权重分布和局部变形表达能力。

Pose-based Validation 使用标准动作：抬手、弯肘、握拳、转头、张嘴、抬腿、深蹲、踮脚。检查 Volume Preservation、Surface Distortion、Self-intersection、Skinning Stability 和 Silhouette Stability。静态网格通过不代表动画通过。

## 7. 工程实现与工具

- Blender / bpy：建模、Shrinkwrap、Remesh、UV、Baking、Rigging 和自动化。
- Instant Meshes：方向场自动重网格化。
- QuadriFlow：自动四边形网格生成。
- ZBrush ZRemesher：雕刻模型自动重拓扑。
- Open3D / Trimesh：几何检查、点云和网格处理。

Blender 常见操作：
- Shrinkwrap：将新网格贴近目标表面；不负责设计 Edge Flow。
- Remesh：重新生成表面网格；Voxel Remesh 不等于角色 Quad Retopology。
- Decimate：减少复杂度，不保证动画拓扑。
- 角色 Retopology：自动基础拓扑 + 关键区域人工修正。

### Blender bpy 教学示例：Decimate
```python
import bpy

source = bpy.context.active_object
if source is None or source.type != "MESH":
    raise RuntimeError("Please select a mesh object")

bpy.ops.object.duplicate()
low = bpy.context.active_object
low.name = source.name + "_processed"

decimate = low.modifiers.new("MeshReduction", "DECIMATE")
decimate.ratio = 0.25

bpy.context.view_layer.objects.active = low
bpy.ops.object.modifier_apply(modifier=decimate.name)

bpy.ops.wm.obj_export(
    filepath="//processed.obj",
    export_selected_objects=True
)
```
此代码是 Mesh Reduction 示例，不是自动 Quad Retopology。

外部工具调用示意：
```python
import subprocess
from pathlib import Path

input_mesh = Path("source.obj")
output_mesh = Path("retopo.obj")
command = [
    "instant-meshes", str(input_mesh),
    "-o", str(output_mesh), "-f", "30000"
]
result = subprocess.run(
    command, capture_output=True, text=True, timeout=600
)
if result.returncode != 0:
    raise RuntimeError(result.stderr)
if not output_mesh.exists():
    raise RuntimeError("Retopology output missing")
```
命令行参数必须以实际安装版本的 --help 为准；该代码是集成示意，不保证适用于所有编译版本。

## 8. AI Agent Workflow

1. Mesh Analyzer：检查面数、拓扑、曲率、边界和法线。
2. Task Planner：判断静态道具、角色、面部动画或其他用途。
3. Strategy Selection：选择 QEM、Instant Meshes、QuadriFlow、Guided Retopology 或人工方案。
4. Execution：运行工具并记录参数。
5. Validation：几何误差、拓扑、面数、边流、UV、烘焙。
6. Failure Diagnosis：按失败类型调整参数或切换策略。
7. Human-in-the-loop：高风险结果人工审批。
8. Delivery：输出模型、配置、报告和可追溯证据。

Agent 的价值不只是 Tool Calling，而是任务判断、工具编排、质量验证和异常恢复。

## 9. 评价体系

### Geometric Fidelity
双向 Chamfer Distance：
[
CD(P,Q)=\frac1{|P|}\sum_{p\in P}\min_{q\in Q}\|p-q\|^2+
\frac1{|Q|}\sum_{q\in Q}\min_{p\in P}\|q-p\|^2
]
需统一坐标、尺度、采样和距离协议。

### Hausdorff Distance
[
d_H(P,Q)=\max\{\sup_{p\in P}\inf_{q\in Q}d(p,q),\sup_{q\in Q}\inf_{p\in P}d(p,q)\}
]
关注最坏情况偏差，对离群点敏感，可报告 P95 等分位数。

### Normal Consistency
[
NC=\frac1N\sum_i n_i^{high}\cdot n_i^{low}
]
需要先建立可靠表面对应关系，不能直接比较不同模型任意顶点的法线。

### Mesh Quality
Triangle/Quad Aspect Ratio、Edge Length Distribution、Minimum/Maximum Angle、Scaled Jacobian、Degenerate Faces。长条面不必然错误，需结合曲面方向和用途。

### Topology Quality
统计 Valence Distribution、Non-manifold Edges、Boundary Edges、Singularities、Connected Components、Self-intersection。

### Feature Preservation
Curvature Error、Silhouette Error、Sharp Feature Preservation。

### Deformation Quality
使用统一 Rig、Skinning、Pose 和参考标准，评价 Volume Change、Surface Distortion、Penetration、Silhouette 和动画稳定性。

### UV / Baking
检查 UV Overlap（区分有意镜像重叠）、Stretching、Padding、Seam、Normal Baking Error 和 Texture Completeness。

### Production Efficiency
Face Count、Processing Time、UV Pass、Bake Pass、Rig Pass、Engine Import Pass、Production Pass Rate。

## 10. 实际案例：AI 角色进入 UE
1. 分析源模型：面数、法线、连通性、非流形、自相交、UV。
2. 设定目标面数预算（示例 30,000 triangles，不是行业标准）。
3. 语义分区：Head、Torso、Arms、Hands、Legs、Hair、Clothing、Accessories。
4. 自动生成基础拓扑，再人工修正面部、肩膀、肘部、膝盖和手指。
5. Shrinkwrap 贴合高模。
6. UV Unwrapping、Cage、Normal/AO/Curvature Baking。
7. Rigging、Skinning、BlendShape（如需要）。
8. Idle/Walk/Run/Jump/Attack/Facial Expression 测试。
9. UE 导入、材质、骨骼、动画、碰撞、性能和 LOD 验收。

## 11. 面试追问

1. Retopology 是什么？
2. Retopology 与 Mesh Simplification 区别？
3. 为什么角色需要 Quad Topology？
4. 什么是 Edge Flow？
5. Vertex Valence 是什么？
6. Half-edge 是什么？
7. QEM 的推导与 Edge Collapse 代价如何计算？
8. Orientation Field 是什么？
9. Instant Meshes 的原理？
10. QuadriFlow 相比 Instant Meshes 的改进？
11. 为什么自动重拓扑不保证动画质量？
12. Shrinkwrap 的作用与局限？
13. High-to-Low Baking 是什么？
14. 拓扑如何影响 Skinning？
15. 如何设计 Retopology Benchmark？
16. 如何让 Agent 自动执行并验收重拓扑？

## 12. 小测

基础题：
1. Retopology 的目标是什么？
2. Mesh Simplification 与 Retopology 有何区别？
3. 规则 Quad Mesh 普通内部顶点通常是多少 Valence？
4. Half-edge Twin 表示什么？
5. QEM 主要解决什么问题？
6. Instant Meshes 如何引导网格方向？
7. Normal Map 能否改变真实几何轮廓？
8. 为什么需要 Pose-based Validation？
9. QuadriFlow 为什么关注奇异点？
10. Chamfer 低能否证明动画质量好？

高阶题：
1. 将 500,000 三角面 AI 角色处理为游戏资产，设计完整方案并解释为何不能只用 QEM。
2. 从平面方程推导 QEM 的 Kp、Qv 和 Edge Collapse 误差。
3. 为腾讯混元建立自动重拓扑 Benchmark：数据集、算法对比、指标、失败分类和生产验收。

建议评分：概念 15%，数据结构 15%，算法 25%，工程 20%，评测和生产 25%。完成小测和实践后才能标记 mastered。

## 参考资料
- Garland & Heckbert, Surface Simplification Using Quadric Error Metrics, SIGGRAPH 1997.
- Jakob et al., Instant Field-Aligned Meshes, SIGGRAPH Asia 2015. https://rgl.epfl.ch/publications/Jakob2015Instant
- Huang et al., QuadriFlow: A Scalable and Robust Method for Quadrangulation, 2018. https://stanford.edu/~jingweih/papers/quadriflow/
- Blender Manual: https://docs.blender.org/manual/en/latest/
- Blender Python API: https://docs.blender.org/api/current/
- Open3D: https://www.open3d.org/
- Trimesh: https://trimesh.org/

## 图片与图示清单
本讲聊天内容中的图片为图片查询/示意图，不等于已取得原始二进制图片。原始图片文件未随本 Markdown 自动归档。恢复时需逐一核对原始图像、顺序和出处：
1. High-poly sculpt vs clean low-poly retopology.
2. Face / eye / mouth edge loops.
3. Triangle / Quad / N-gon topology.
4. Vertex valence 3/4/5.
5. Curvature visualization.
6. Half-edge structure.
7. UV seams and checker texture.
8. Edge Collapse before/after.
9. QEM plane error.
10. Instant Meshes orientation field.
11. QuadriFlow singularity comparison.
12. Shrinkwrap high/low mesh.
13. High-to-low normal baking and cage.
14. Tangent-space vs object-space normal.
15. Rigging, skinning and joint deformation.
16. Blender, Instant Meshes, QuadriFlow, ZRemesher, Open3D and Trimesh interfaces.
17. Retopology Benchmark examples.
18. AI character to Unreal Engine production pipeline.
