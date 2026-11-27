# 第 22 讲：当前撰写源稿与交付证据

日期：2026-11-28（Asia/Shanghai）。主题：Training Dataset Construction。

## 来源与精确性

- `transcript.md` 保存本次最终教学回复的完整撰写源稿，状态为 **authored-current-turn**。它包含九段教学链、全部公式/表格/代码片段、8 组面试问答及追问、10 道客观题及解释、3 道分析题及参考答案/评分、4 项动手作业、参考资料和交付说明。
- 这是源稿保留，不冒充从聊天界面独立导出的历史消息。独立 UI 导出一致性仍为 **unverified**。
- `user-request.md` 保存本讲实际用户请求；`progress-messages.md` 按顺序保存本次进度消息，包装标题不属于原消息。
- `lessons/lesson-22-training-dataset-construction.md` 是 GitHub 可读版。唯一转换为删除 GenUI 引用显示标记，保留全部文字、空白及 [R1]–[R9] 参考链接。`citation-map.json` 保存精确标记与位置，可逆还原完整源稿；已作本地往返相等核对。
- 不以本讲新编源稿宣称第 1–18 讲历史原文/图片恢复完成；第 13、17 讲缺失状态保持不变。

## 图示、代码与实际执行

- `assets/dataset-construction-flow.mmd` 与正文 Mermaid 代码块逐字一致。本讲没有使用外部或生成的图片二进制；流程图源码完整保留。
- `examples/lesson22/dataset_construction_lab.py` 为完整可运行脚本，`README.md` 说明输入、命令、结果和限制，`example-report.json` 为实际完整标准输出。
- `execution-verification.json` 记录整合者审阅代码后独立复跑的命令、环境、退出码、源码/报告摘要和八项故障检查；标准输出与报告相同，且与此前独立执行报告一致。
- 合成实验没有真实 Mesh、神经网络训练、未知近重复发现、域外/时间外评估或置信区间计算。它不证明真实 3D 泛化效果。
- 维护者运行实验不等于学习者完成练习，个人状态保持 taught、未验收。

## 发布核验

`source-manifest.json` 记录本次内容文件的摘要与范围。它排除自身以及后生成的 `delivery-verification.json`，避免循环摘要。

`delivery-verification.json` 在内容提交并逐份远程回读后生成，记录实际提交、路径、内容相等和未涉及文件保留情况。阅读该记录才能确认发布范围，不能仅凭此 README 或文件存在推断成功。发布后追加的进度消息与相应 manifest 更新作为元数据后续提交。

本讲继续沿用仓库六门课程、51 个知识单元的规划。下一讲为第 23 讲 Hard Sample Mining；必须保护开发与最终测试的边界。
