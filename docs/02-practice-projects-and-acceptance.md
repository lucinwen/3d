# 六课程实践项目与阶段验收规划

## 总体路径

采用“基础理解 → 单元练习 → 课程项目 → 综合面试”的递进方式。每阶段先建立可复现输入，再实现流程，最后用指标和失败案例验收。

## 课程 1：3D Asset Inspector

### 目标
制作一个 Blender Python 资产检查器，并输出统一 JSON 报告。

### 模块
- Geometry/Topology：顶点、边、面、退化面、边界边、非流形、连通组件。
- UV：UV Layer、重叠、拉伸、Texel Density。
- Material：节点、贴图路径、色彩空间、材质槽。
- Rig/Animation：骨骼存在性、权重和、标准动作测试。
- Rendering：固定相机/光照输出 RGB、Depth、Normal、Mask。
- Delivery：导出、资源依赖和 UE 导入验证。

### 验收
- 同一批资产重复运行结果可复现。
- 每条规则有 severity、evidence、asset_id、tool_version。
- 自动检测与人工复核边界清晰。
- 不能把未实现的检测写成 PASS。

## 课程 2：Text/Image-to-3D 路线对比

### 目标
选择一组代表性 Prompt 和参考图片，比较至少两种生成/重建路线。

### 实验记录
- 输入图像/Pprompt、模型名称和版本。
- 分辨率、随机种子、生成参数、耗时和显存。
- 输出表示类型（Mesh/NeRF/3DGS/Point Cloud 等）。
- 是否需要 Mesh Extraction、Retopology、UV 和纹理后处理。
- 多视角渲染和失败类型。

### 验收
- 明确区分生成与真实重建。
- 有 Ground Truth 时才报告对应几何误差。
- 记录不可见表面属于观测还是先验推断。
- 比较视觉质量与生产通过率，不以单一 CLIP 分数排名。

## 课程 3：3D Data Dataset Pipeline

### 目标
建立可追溯的数据集规范和自动化清洗流水线。

### 模块
- Source Registry：来源、授权、许可、采集日期。
- Canonicalization：格式、坐标系、单位、尺度和属性标准化。
- Validation：文件解析、几何、纹理和元数据检查。
- Deduplication：SHA-256 精确去重、感知/几何近重复检测。
- Annotation：类别、部件、材质、风格、空间关系、置信度。
- Dataset Split：按原始资产/身份分组，防止派生版本泄漏。
- Lineage：父子关系、处理工具、参数和版本。

### 验收
每个样本可追溯来源、处理记录、标注版本和数据集归属；拒收原因可统计。

## 课程 4：3D Benchmark

### 目标
为一个明确任务定义 Benchmark，而不是堆砌指标。

### 模块
- Task Card：输入、输出、适用场景、失败定义。
- Test Set：分层样本、长尾与困难样本。
- Metrics：几何、视觉、语义、相机、生产指标。
- Human Study：盲测、随机化、评分量表和评测者校准。
- Statistics：置信区间、效应量、Kappa/ICC 的正确选择。
- Reporting：总体结果、分层结果、失败案例、局限。

### 验收
- 指标与任务目标对应。
- 坐标、尺度、采样和阈值协议公开。
- 有 GT/无 GT 两套评价策略。
- 结论不超出指标证据范围。

## 课程 5：Game Production / TA

### 目标
将生成角色和场景送入 Unreal Engine 的生产验证流程。

### 模块
- Character：Rig、Skin、Morph、Animation、Spring Bone。
- Scene：坐标、碰撞、拓扑连通、空间语义、可达性。
- Engine：导入、材质、LOD、资源引用、性能。
- Validation：标准动作、标准场景、自动截图和缺陷分类。

### 验收
- 角色通过规定动作集。
- 资产满足目标项目的性能预算。
- 场景满足功能、动线和空间约束。
- 所有通过结论有可复核证据。

## 课程 6：3D Agent Harness

### 目标
建立一个可恢复、可审计的 Agent 工作流，能够调用 DCC/重建/引擎工具并自动验收。

### 状态机建议
`RECEIVED → PLANNED → GENERATING → PROCESSING → VALIDATING → REPAIRING → REVALIDATING → DELIVERED`
失败分支：
`BLOCKED / NEEDS_HUMAN / FAILED`

### 必备能力
- Tool schema 和参数校验。
- 任务依赖图与并行策略。
- 任务状态、检查点和版本。
- 幂等执行与重试策略。
- 工具超时、错误分类和异常恢复。
- 自动验收断言与证据保存。
- 低置信度人工审批。
- 审计日志和可复现报告。

### 验收
- 中断后可从检查点续跑。
- 重试不会重复产生不可控副作用。
- 工具失败与模型质量失败分开记录。
- 每次交付包含资产、版本、报告和证据。

## 综合结业项目：3D Generation Quality & Agent Workbench

输入：文本或参考图片。
流程：条件解析 → 3D 生成/重建 → 资产处理 → 自动评测 → 缺陷归因 → 修复/人工复核 → 回归测试 → 导出。
输出：3D 资产、评测报告、数据血缘、运行日志和可复现配置。

## 面试结业验收

候选人需要能够：
1. 白板解释一个算法的原理和公式。
2. 解释数据结构和坐标/单位约定。
3. 运行一个工程工具并解释输出。
4. 设计可复现的评测协议。
5. 诊断失败样本并提出验证实验。
6. 解释自动化边界、异常恢复和人工介入点。
