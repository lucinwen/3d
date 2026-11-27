# 第十五讲：Shape Generation（3D 形状生成）

> 课程 2：3D 生成模型与重建  
> 状态：教学稿已讲授并归档；学习者尚未完成小测和实践验收。  
> 本讲目标：理解 Shape Representation、Shape Space、Shape Generation 架构、数据治理、几何评价和生产验收。

## 1. 概念

Shape Generation 是学习三维形状分布并生成新形状的任务。若 S 表示形状，模型学习 pθ(S)；若有文本/图片/部分几何条件 c，则学习 pθ(S|c)。

区分：
- Shape Reconstruction：从观测恢复已有物体。
- Shape Generation：从噪声、潜在变量或条件生成新形状。
- Shape Completion：从部分观测推断完整形状；未观测区域是模型推断，不应冒充真实观测。
- Visual Plausibility、Geometric Validity、Production Readiness 是不同层次。

Shape Space：将形状编码为 z∈R^d，模型可在潜在空间学习形状分布。潜在距离不天然等于人类感知相似度，必须通过任务验证。

## 2. 原理：五种表示

### 2.1 Voxel
V∈R^(Nx×Ny×Nz)，体素可存 Occupancy、Density、RGB、Semantic Label 或 SDF。规则网格便于 3D CNN，但空间内存随分辨率立方增长。256³ 单通道 float32 约 64 MiB，512³ 约 512 MiB（仅原始数值）。

### 2.2 Point Cloud
P={p_i}，p_i=(x_i,y_i,z_i)，通常 P∈R^(N×3)。点集无固定顺序，因此网络应满足排列不变性/等变性。PointNet 使用共享 MLP 提取点特征，再通过对称聚合（如 max pooling）形成排列不变的全局特征。点云不直接包含面片拓扑，常需表面重建。

### 2.3 Mesh
M=(V,F)，V 为顶点坐标，F 为面片索引。生成 Mesh 不仅要生成顶点位置，还要处理连接关系、顶点数、面数、非流形、自相交和拓扑变化。固定拓扑任务与可变拓扑任务难度不同。

### 2.4 Implicit Representation
学习 fθ(x) 这样的连续空间函数。Occupancy 可输出占据概率/值，表面由阈值边界定义；SDF 输出有符号距离，表面由 f(x)=0 定义；NeRF density 是体密度，不等于 SDF。隐式表示不直接存储标准 Mesh 拓扑，提取表面后仍需资产处理。

### 2.5 Latent Shape Representation
Encoder 将形状映射为 z，Decoder 从 z 恢复形状。潜在表示可供 VAE、GAN、Autoregressive、Diffusion 等生成模型使用。

## 3. 生成架构

### 3.1 Autoencoder
S → Encoder → z → Decoder → S_hat。训练重建损失。普通 AE 不保证潜在空间服从可直接采样的先验分布。

### 3.2 VAE
qφ(z|x)=N(μφ(x), diag(σφ²(x)))。重参数化：
[
z=\mu+\sigma\odot\epsilon,\quad\epsilon\sim N(0,I)
]
典型目标：
[
L=L_{recon}+\beta D_{KL}(q_\phi(z|x)\|p(z))
]
推理时从先验采样 z，再经 Decoder 生成。注意重建质量与生成质量不同；可能出现过平滑或 Posterior Collapse。

### 3.3 GAN
Generator 从 z 生成形状，Discriminator 区分真实与生成样本。经典 min-max 目标：
[
\min_G\max_D E_{S\sim p_{data}}[\log D(S)]+E_{z\sim p(z)}[\log(1-D(G(z)))]
]
风险包括训练不稳定和 Mode Collapse（只生成少量相似形状）。

### 3.4 Autoregressive
将形状编码为 Token 序列：
[
p(t_1,\ldots,t_N)=\prod_i p(t_i|t_{<i})
]
按序生成 Voxel/Mesh/Shape Tokens。优势是序列建模；局限是顺序采样成本、tokenization 信息损失和序列长度。

### 3.5 Diffusion
对所选形状表示 S0 加噪：
[
S_t=\sqrt{\bar\alpha_t}S_0+\sqrt{1-\bar\alpha_t}\epsilon
]
网络学习反向去噪。可用于 Voxel、Point Cloud、SDF Grid、Latent 等；不同表示仍需专门处理排列、拓扑、距离场等约束。

## 4. 代表性研究

- ShapeNet：大规模类别化三维模型资源。使用时检查类别分布、重复、来源、许可、尺度、坐标系和数据泄漏。
- PointNet：共享点 MLP + 对称聚合处理无序点集；它主要是点云理解架构，不应误称为通用生成模型。
- Occupancy Networks：将三维表面表示为神经网络分类器的连续决策边界。
- DeepSDF：用形状 Latent Code 和查询点预测连续 SDF；Auto-Decoder 训练联合优化形状潜在码与解码器。
- GET3D：NeurIPS 2022，形状和纹理潜在编码，结合 SDF、DMTet、纹理场和可微渲染，生成显式纹理 Mesh。显式 Mesh 输出更接近 DCC/游戏资产格式，但仍需拓扑、UV、材质、LOD、碰撞和引擎验收。
- DG3D：ICCV 2023，研究扩散增强的三维纹理 Mesh 生成。

## 5. 数据结构与数据治理

建议资产记录至少包含：
- asset_id、category、source、license、source_asset_id。
- vertices/faces/normals/materials/textures。
- scale、unit、coordinate_system、up_axis、front_axis、origin convention。
- file_hash、processing_version、annotation_version、dataset_split。
- geometry_quality、topology_quality、validation_evidence。

质量检查：
- Empty Mesh、NaN/Inf、Degenerate Faces、Duplicate Vertices。
- Non-manifold Edges、Normal Orientation、Self-intersection。
- Connected Components、Watertightness（按用途判断）。
- Texture/Material 引用、UV 完整性。

去重：
- SHA-256 精确文件去重。
- 归一化几何、采样点云、Chamfer/形状描述子用于近重复候选检测。
- 几何近似相同不必然是重复资产，需考虑纹理和设计差异。

标准化：
[
x'=x-c,\quad x''=x'/s
]
其中 c 是选定中心，s 是尺度因子。必须明确单位、坐标系、朝向、原点和归一化策略，避免破坏真实尺度或语义比例。

Train/Val/Test 应按原始资产、来源或身份分组，防止同一资产的变体跨集合造成数据泄漏。

## 6. 算法与工程实践

### 6.1 Point Cloud Autoencoder 教学实验
- 采样点云 P∈R^(N×3)。
- Encoder 使用共享 MLP，沿点维度做 max pooling 得到 latent。
- Decoder 从 latent 输出 N 个三维点。
- 使用双向 Chamfer Distance 训练。
- 单个球体样本只能验证代码链路，不能证明模型学会了类别级 Shape Generation。

### 6.2 Chamfer Distance 教学实现
[
CD(P,Q)=\frac1{|P|}\sum_{p\in P}\min_{q\in Q}\|p-q\|^2+
\frac1{|Q|}\sum_{q\in Q}\min_{p\in P}\|q-p\|^2
]
朴素 torch.cdist 实现计算/显存成本高，大规模任务应使用分块或高效 CUDA 最近邻算子。

### 6.3 Latent Interpolation
[
z(t)=(1-t)z_A+tz_B
]
观察形状变化连续性、结构断裂、自相交和异常部件。球面潜在先验有时使用 Slerp。潜在插值连续不保证拓扑合理。

### 6.4 Completion
[
S_{complete}\sim p_\theta(S|S_{partial})
]
应区分观测区域和推断区域，记录置信度/来源，不把生成补全冒充真实扫描。

## 7. 评价指标

几何：
- Chamfer Distance：双向最近邻距离；受采样密度、坐标、尺度和平方/非平方协议影响。
- F-score：在阈值 τ 下综合 Precision/Recall。
- Normal Consistency：法线方向一致性。
- IoU：适用于统一对齐的占据体素/体积。

分布和多样性：
[
MMD=\frac1{|S_{ref}|}\sum_{S\in S_{ref}}\min_{\hat S\in S_{gen}}D(S,\hat S)
]
Coverage/COV 统计真实样本被多少不同生成样本作为最近邻匹配。MMD 越低通常越好，COV 越高通常越好；必须结合几何质量和多样性分析。

生产：
- Connected Components、Boundary Edges、Non-manifold、Self-intersection、Watertightness（按任务）。
- UV/Material/LOD/Collision/Engine Import Pass Rate。
- Production Pass Rate = 通过规定生产验收的资产数 / 生成资产总数。

无 Ground Truth 时，不得宣称真实 CD/F-score；使用代理指标时应明确标记为 proxy。

## 8. 实际案例：游戏道具生成

输入文本/图像/多视图条件 → Condition Encoder → Shape Generator（Latent Diffusion / Mesh Generator / Implicit Model）→ Geometry Decoder/Surface Extraction → Mesh Cleanup/Retopology → UV/Material/Texture → Automated QA → Unreal Engine Validation。

质量门禁：
1. 输入条件解析。
2. 生成结构和条件一致性。
3. 几何、尺度和坐标检查。
4. 拓扑检查。
5. UV/材质检查。
6. 引擎导入、碰撞、性能检查。
7. 人工审批和回归测试。

交付应包含源几何、生产 Mesh、贴图、生成配置、条件、模型版本、元数据、验证报告和多视角预览。

## 9. 面试追问

1. Shape Generation 与 Reconstruction 有何区别？
2. Voxel、Point Cloud、Mesh、Implicit 各自的取舍？
3. PointNet 如何处理排列不变性？
4. 为什么 Mesh Generation 比点云生成复杂？
5. Autoencoder 与 VAE 有何区别？
6. GAN Mode Collapse 是什么？
7. GET3D 的 SDF、DMTet、Texture Field 如何协作？
8. 为什么 CD 低仍可能拓扑不合格？
9. MMD 和 COV 分别衡量什么？
10. 如何提高生产通过率？

## 10. 小测

基础题：
1. Shape Generation 的目标是什么？
2. Voxel 与 Point Cloud 的数据结构差异？
3. 为什么点云需要排列不变性？
4. Mesh 生成为什么涉及拓扑？
5. VAE 重参数化解决什么问题？
6. GAN Mode Collapse 是什么？
7. 普通 AE 为什么不保证潜在空间可采样？
8. GET3D 的核心设计是什么？
9. MMD 衡量什么？
10. CD 低能否证明拓扑合格？

开放题：
1. 比较 Voxel、Point Cloud、Mesh、SDF 四种表示，为椅子、汽车、人物生成选择主表示并论证。
2. CD 很低但多样性不足且 Mesh 有非流形边/自相交，设计评测和改进方案。
3. 参考 GET3D 设计面向游戏资产生产的 Shape Generation 系统，覆盖数据、Shape/Texture、生成、表面提取、质量门禁和交付。

评分：概念 20%，表示与数据结构 20%，生成算法 20%，评价 20%，工程生产 20%。完成测验和实践后才能标记 mastered。

## 参考资料
- ShapeNet: An Information-Rich 3D Model Repository. https://arxiv.org/abs/1512.03012
- PointNet. https://arxiv.org/abs/1612.00593
- Occupancy Networks. https://arxiv.org/abs/1812.03828
- DeepSDF. https://arxiv.org/abs/1901.05103
- GET3D. https://arxiv.org/abs/2209.11163
- DG3D. https://openaccess.thecvf.com/content/ICCV2023/papers/Zuo_DG3D_Generating_High_Quality_3D_Textured_Shapes_by_Learning_to_ICCV_2023_paper.pdf
- A Survey of Deep Learning-based 3D Shape Generation. https://link.springer.com/article/10.1007/s41095-022-0321-5
