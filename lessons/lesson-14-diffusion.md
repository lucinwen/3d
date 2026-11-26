# 第 14 讲：Diffusion（扩散模型）

> 课程 2：3D 生成模型与重建  
> 状态：教学稿已归档；学习者尚未完成测验与实践验收。  
> 本讲采用 DDPM 作为数学主线，再连接 DDIM、Score Matching、CFG、Latent Diffusion 与 3D Diffusion。

## 1. 概念

生成模型学习数据分布并生成新样本。Diffusion Model 先定义一个逐步加噪的前向过程，再训练神经网络学习反向去噪过程。生成时从简单先验（通常为标准高斯噪声）出发，逐步恢复样本。

必须区分：
- Forward Diffusion：人为设计的加噪过程。
- Reverse Diffusion：学习得到的反向生成过程。
- Training：训练网络预测噪声或其他参数化目标。
- Sampling：使用训练好的网络从噪声逐步生成数据。

## 2. 原理

### 2.1 高斯噪声与时间步

`epsilon ~ N(0,I)`。离散时间步 `t=0,...,T`，其中 x0 是干净数据，xT 通常接近标准高斯噪声。

### 2.2 前向过程

定义：
[
\alpha_t=1-\beta_t,\qquad
\bar\alpha_t=\prod_{s=1}^{t}\alpha_s
]
单步加噪：
[
q(x_t|x_{t-1})=N(\sqrt{\alpha_t}x_{t-1},\beta_t I)
]
等价采样：
[
x_t=\sqrt{\alpha_t}x_{t-1}+\sqrt{\beta_t}\epsilon
]
利用高斯线性组合，可以直接从 x0 采样任意 t：
[
q(x_t|x_0)=N(\sqrt{\bar\alpha_t}x_0,(1-\bar\alpha_t)I)
]
[
\boxed{x_t=\sqrt{\bar\alpha_t}x_0+\sqrt{1-\bar\alpha_t}\epsilon}
]
因此训练时不需要逐步执行所有前向时间步。

### 2.3 Noise Schedule

Beta Schedule 决定每一步加噪强度。常见有 Linear、Cosine 等设计。Beta Schedule 是前向噪声设计；推理时选择哪些时间步、如何求解反向轨迹，是 Sampling Schedule/Solver 的问题，二者不可混淆。

### 2.4 DDPM 噪声预测训练

训练时采样 x0、随机时间步 t 和噪声 epsilon，构造 xt，然后让网络预测 epsilon：
[
\hat\epsilon=\epsilon_\theta(x_t,t)
]
经典简化损失：
[
\boxed{L_{simple}=E_{x_0,t,\epsilon}[\|\epsilon-\epsilon_\theta(x_t,t)\|_2^2]}
]
从噪声预测可恢复干净样本估计：
[
\hat x_0=\frac{x_t-\sqrt{1-\bar\alpha_t}\epsilon_\theta(x_t,t)}{\sqrt{\bar\alpha_t}}
]

### 2.5 DDPM 反向过程

[
p_\theta(x_{t-1}|x_t)=N(\mu_\theta(x_t,t),\Sigma_\theta(x_t,t))
]
常见固定方差 DDPM 反向均值：
[
\mu_\theta=\frac1{\sqrt{\alpha_t}}
\left(x_t-\frac{\beta_t}{\sqrt{1-\bar\alpha_t}}\epsilon_\theta(x_t,t)\right)
]
再按选定方差添加随机项。不同 DDPM 实现可以采用不同方差参数化，不能把单一实现当成所有扩散模型的统一形式。

### 2.6 Score Matching

Score Function：
[
s(x)=\nabla_x\log p(x)
]
在高斯扰动条件下，噪声预测与 Score 估计有关系：
[
s_\theta(x_t,t)\approx-\frac{\epsilon_\theta(x_t,t)}{\sqrt{1-\bar\alpha_t}}
]
Score 指向对数概率密度增长最快的方向。Score-based 方法可使用反向 SDE 或 Probability Flow ODE 等连续时间形式进行生成。

### 2.7 SDE

一般随机微分方程：
[
dx=f(x,t)dt+g(t)dw
]
f 是 drift，g 是 diffusion coefficient，w 是 Brownian motion。连续时间 Score-based Generative Modeling 将不同噪声尺度下的生成过程统一到 SDE 框架中。

## 3. 数据结构

训练批次通常包含：
- clean sample x0；
- timestep t；
- sampled noise epsilon；
- noisy sample xt；
- optional condition c（文本、图像、类别、深度、姿态等）；
- prediction target（epsilon、x0 或 v）。

三种常见参数化：
- epsilon-prediction：预测噪声。
- x0-prediction：预测干净样本。
- v-prediction：预测信号与噪声的组合变量。

常见 v 定义：
[
v_t=\sqrt{\bar\alpha_t}\epsilon-\sqrt{1-\bar\alpha_t}x_0
]
可反解：
[
x_0=\sqrt{\bar\alpha_t}x_t-\sqrt{1-\bar\alpha_t}v_t
]
[
\epsilon=\sqrt{1-\bar\alpha_t}x_t+\sqrt{\bar\alpha_t}v_t
]

## 4. 算法

### 4.1 DDPM
经典训练：随机抽取 x0、t、epsilon，构造 xt，网络预测噪声，使用 MSE 等目标更新网络。采样：从 xT~N(0,I) 开始，按反向时间步迭代。

### 4.2 DDIM
DDIM 可在复用 DDPM 训练目标的基础上构造非马尔可夫采样轨迹，减少采样步数。常见更新形式：
[
x_s=\sqrt{\bar\alpha_s}\hat x_0+
\sqrt{1-\bar\alpha_s-\sigma_t^2}\hat\epsilon+
\sigma_t z
]
其中 s<t，sigma 控制随机性。sigma=0 时可得到确定性采样轨迹。采样步数减少可能影响质量，必须实验验证。

### 4.3 CFG
Classifier-Free Guidance 在训练中以一定概率丢弃条件，使网络学会有条件和无条件预测。推理时：
[
\epsilon_{guided}=\epsilon_{uncond}+w(\epsilon_{cond}-\epsilon_{uncond})
]
w 控制条件引导强度。过高可能导致多样性下降、过饱和或结构失真。CFG 不等于简单提高文本权重。

### 4.4 网络架构
经典图像扩散常使用 U-Net：Encoder、Bottleneck、Decoder 和 Skip Connections。Timestep Embedding 让网络知道当前噪声阶段。Cross-Attention 常用于把文本条件注入图像特征：
[
Attention(Q,K,V)=Softmax(QK^T/\sqrt d)V
]
Self-Attention 的 Q/K/V 来自同一特征序列；Cross-Attention 的 Q 来自当前特征，K/V 来自条件特征。也存在 DiT 等 Transformer 架构，并非所有扩散模型都必须使用 U-Net。

### 4.5 Latent Diffusion
VAE Encoder 将图片 x 压缩为 latent z；扩散在 latent 空间中进行；最终由 VAE Decoder 解码回图像。经典 VAE 可用：
[
q_\phi(z|x)=N(\mu_\phi(x),diag(\sigma_\phi^2(x)))
]
重参数化：
[
z=\mu+\sigma\odot\epsilon
]
潜在扩散减少空间计算规模，但压缩可能损失细节；VAE 的训练目标和实现依模型而异。

### 4.6 3D Diffusion 表示路线
- Voxel Diffusion：规则体素网格；易用 3D CNN，但高分辨率内存昂贵。
- Point Cloud Diffusion：对点坐标/特征去噪；必须考虑点集排列不变性、密度和表面重建。
- Mesh Diffusion：生成顶点/面片或 Mesh latent；需要处理拓扑、顶点数和连接关系。
- SDF Diffusion：生成距离场，再用零水平集和 Marching Cubes 提取表面；需要检查符号、距离性质和提取质量。
- Latent 3D Diffusion：先压缩三维表示，再在潜在空间扩散。

## 5. 工程实现

### 5.1 最小前向加噪代码
```python
import torch

def q_sample(x0, t, alpha_bars):
    noise = torch.randn_like(x0)
    a_bar = alpha_bars[t].view(
        -1, *([1] * (x0.ndim - 1))
    )
    xt = a_bar.sqrt() * x0 + (1 - a_bar).sqrt() * noise
    return xt, noise
```
前提：t 是 batch 内每个样本的离散时间步索引；alpha_bars 已移动到相同 device；x0 的数值范围与模型训练约定一致。

### 5.2 训练闭环
1. 读取干净样本 x0。
2. 随机采样 t。
3. 采样 epsilon。
4. 构造 xt。
5. 将 xt、t 和可选条件 c 输入去噪网络。
6. 预测 epsilon（或其他明确的 prediction type）。
7. 与对应 target 计算损失。
8. 反向传播并更新参数。

### 5.3 推理闭环
1. 从先验噪声初始化。
2. 根据 scheduler 选择时间步。
3. 调用网络预测。
4. 根据 prediction type 转换为所需量。
5. 使用 sampler 更新状态。
6. 重复直到最终样本。
7. 若为 Latent Diffusion，最后使用 Decoder 解码。

### 5.4 排障
- 训练不收敛：检查数据归一化、噪声 schedule、时间步索引、预测目标和学习率。
- 生成全噪声：检查训练/推理 prediction type、scheduler 配置、权重和归一化。
- 条件不遵循：检查文本编码、条件丢弃训练、Cross-Attention、CFG scale。
- 结构错误：检查数据质量、训练集覆盖、模型容量和条件信息。
- 3D 结果差：检查表示、坐标系、几何约束、采样与表面提取，不能只看图像指标。

## 6. 评价指标

图像生成：
- FID：真实与生成图像特征分布距离，通常越低越好；依赖 Inception 特征和样本协议。
- IS：类别可辨识性和多样性代理指标；有局限。
- CLIP Score：文本与图像语义相似度；不证明细粒度空间关系正确。
- LPIPS：深度特征感知距离，通常越低越好。

3D 生成：
- Chamfer Distance、F-score、Normal Consistency、IoU（按表示和 GT 选择）。
- 几何完整性、部件/语义关系、跨视角一致性。
- 多样性与 Coverage。
- Mesh/Topology/UV/Engine Pass Rate。

效率：
- Sampling Steps、Latency、Throughput、GPU Memory、Model Size。

必须按任务定义指标；FID 不能证明 3D 几何正确，CLIP 不能证明拓扑正确。无 GT 几何时不得声称获得真实几何误差。

## 7. 实际案例

图像条件角色生成：
1. 输入角色参考图和文本描述。
2. 图像/文本编码器产生条件特征。
3. 选择 Point Cloud、SDF、Mesh Latent 等 3D 表示。
4. 条件扩散生成三维表示。
5. 进行几何提取、表面修复和多视角渲染。
6. 评价条件遵循、几何准确性、跨视角一致性和生产通过率。
7. 通过 Retopology、UV、材质、Rig、Skinning 和 UE 验收。

多视角生成图片看起来一致，不代表几何一定一致；必须使用跨视角几何和生产测试验证。

## 8. 面试追问

1. Diffusion 的前向和反向过程是什么？
2. 为什么训练时预测噪声？
3. Beta、Alpha、Alpha Bar 有什么区别？
4. DDPM 和 DDIM 有什么区别？
5. Score Function 与噪声预测有什么关系？
6. CFG 的公式和 Guidance Scale 有什么作用？
7. 为什么使用 Latent Diffusion？
8. Cross-Attention 如何注入文本条件？
9. 3D Diffusion 为什么比 2D 更复杂？
10. 怎样评价一个 3D Diffusion 模型的生产可用性？

回答应包含任务目标、数据表示、公式、训练/采样过程、条件融合、评价协议和失败边界。

## 9. 小测

基础题：
1. Forward Diffusion 的作用是什么？
2. Beta、Alpha、Alpha Bar 分别是什么？
3. 如何直接构造任意时间步的 xt？
4. DDPM 的简化训练损失是什么？
5. DDIM 如何减少采样步数？
6. Score Function 是什么？
7. CFG 如何组合有条件和无条件预测？
8. Latent Diffusion 为什么节省计算？
9. Point Cloud Diffusion 为什么需要排列不变性？
10. 为什么 FID 不能证明 Mesh 拓扑正确？

开放题：
1. 推导累计加噪公式，并说明如何从噪声预测恢复 x0。
2. 一个 Text-to-3D 角色背面缺失且 Mesh 自相交，设计条件扩散改进方案和 Benchmark。
3. 设计从 3D 数据采集、清洗、标注、训练、评测、困难样本挖掘到自动验收的 AI Data Pipeline。

评分：概念 20%，数学 25%，算法 20%，工程 20%，评测边界 15%。完成测验和实践后才能标记 mastered。

## 参考论文
- Ho, Jain, Abbeel. Denoising Diffusion Probabilistic Models. NeurIPS 2020. https://arxiv.org/abs/2006.11239
- Song, Meng, Ermon. Denoising Diffusion Implicit Models. https://arxiv.org/abs/2010.02502
- Ho, Salimans. Classifier-Free Diffusion Guidance. https://arxiv.org/abs/2207.12598
- Rombach et al. High-Resolution Image Synthesis with Latent Diffusion Models. https://arxiv.org/abs/2112.10752
- Song et al. Score-Based Generative Modeling through Stochastic Differential Equations. https://arxiv.org/abs/2011.13456
- Luo, Hu. Diffusion Probabilistic Models for 3D Point Cloud Generation. CVPR 2021. https://arxiv.org/abs/2103.01458
