# 第 20 讲工程实验：Task-aware Data Quality Scoring

本实验使用 5 条人工构造记录和两套任务 Profile，验证硬门禁、任务化权重、缺失值与决策分流。它不读取真实 3D 文件，不训练质量模型，也不代表生产阈值。

依赖：Python 3.10+，仅标准库。

~~~bash
python examples/lesson20/quality_scoring_lab.py --output examples/lesson20/example-report.json
~~~

每条资产记录含 asset_id、维度分数和硬门禁。分数为 0–100 的教学值；None 表示未观测。两个 Profile 为 static_classification 与 character_animation。输出原始加权分、权重覆盖率、分维度贡献、缺失维度、门禁失败、决策和原因。calibrated_probability 始终为 null，因为没有独立参考标签。

预期断言：许可门禁失败的样本绝不接受；同一资产在不同任务下可以得到不同分数；缺少必需标注维度的样本进入 review；实验不会虚构概率校准结果。

已知局限：数据完全合成；未实现真实 mesh/texture/rig 检测、概率校准、置信区间、人工审核、资产家族划分和漂移监控。生产使用前必须用独立审核集验证规则和阈值。
