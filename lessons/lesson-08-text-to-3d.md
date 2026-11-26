# 第 8 讲：Text-to-3D

## 1. 概念

Text-to-3D 以自然语言为条件生成三维表示。输出可能是 Point Cloud、Voxel、Mesh、NeRF、3DGS 或潜在表示；生成可渲染三维表示不等于生成可直接进入游戏生产的 Mesh。

## 2. 原理

文本先经过 Tokenization、Embedding 和上下文编码，形成文本条件。生成可分为：
- Optimization-based：对单个样本迭代优化三维表示。
- Feed-forward：训练模型直接预测三维潜在表示/几何。
- Hybrid：结合文本、图像、多视角、三维解码和后处理。

CLIP 通过图像/文本双编码器把两种模态映射到共同语义空间，使用余弦相似度衡量匹配。CLIP 不能直接验证背面几何、拓扑或多视角结构。

## 3. 数据结构

Text Tokens、Text Embeddings、Latent、Camera Pose、3D Representation、Render、Mesh/Texture/Material。必须记录 Prompt、模型版本、采样参数、随机种子（若可用）和输出版本。

## 4. 算法：DreamFusion 与 SDS

DreamFusion（2022）利用预训练 2D Diffusion Model 监督可优化的 NeRF。流程：
1. 初始化三维场景。
2. 采样相机并渲染。
3. 对渲染图加噪。
4. 扩散模型预测噪声。
5. 根据预测噪声与实际噪声的差异构造 SDS 梯度。
6. 经可微渲染将梯度传回三维参数。
7. 迭代优化。

常见 SDS 梯度形式：
[

abla_	heta L approx E[w(t)(epsilon_phi(x_t,t,y)-epsilon)partial I/partial	heta]
]
不同实现的参数化、符号和权重定义可能不同。

Janus Problem 指不同视角出现重复正脸等不一致结构。原因之一是二维先验并不天然保证三维身份一致性。

## 5. 工程实现

Pipeline：Prompt Processing → Text Encoding → 3D Generation → Representation Extraction（如需要）→ Mesh Cleanup → UV/Texture/Material → Validation → Export。伪代码不能冒充可运行模型；每一步需绑定真实模型和接口。

## 6. 评价指标

Text Alignment（CLIP/VLM/人工）、Geometry（CD/F-score/NC）、Multi-view Consistency、Appearance、Structural Usability、Generation Efficiency。CLIP 高分不代表几何正确；无 GT 时不能报告真实 CD。

## 7. 实际案例

“白猫戴蓝色巫师帽”应检查主体、颜色属性绑定、帽子位置、数量、背面结构和多视角一致性。最后还需验证 Mesh、UV、Rig 和 UE 导入。

## 8. 面试追问

- Text-to-3D 与 Text-to-Image 区别？
- CLIP 如何参与三维优化？
- DreamFusion 的贡献是什么？
- SDS 如何把二维监督传到三维？
- 为什么出现 Janus Problem？
- 如何建立 Text-to-3D Benchmark？

## 9. 小测

解释 SDS 公式各项；比较优化式与前向式生成；设计包含文本属性绑定、多视角和生产通过率的 Benchmark。
