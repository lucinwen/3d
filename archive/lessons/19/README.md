# 第 19 讲来源与完整性

本目录保留本次新编第 19 讲的完整授课文本源。它不是对历史聊天的重建，也不是已经从聊天平台独立导出的消息备份。

## 文件

- `transcript.md`：准备交付的完整 assistant 教学文本，包含全部九段、公式、表格、代码摘录、流程图源、8 组面试题和追问答案、10 道客观小测与解析、3 道开放题和参考思路、资料与交付说明。
- `user-request.md`：本次可见用户请求的文本留存；平台消息 ID 不可用。
- `citation-map.json`：普通 Markdown 引用与聊天 GenUI 引用的对应；其余正文保持一致。
- `assets/annotation-review-flow.mmd`：从正文逐字提取的 Mermaid 流程图源。
- `source-manifest.json`：出处、范围、精确性边界、SHA-256 和已执行实验状态。
- `asset-manifest.csv`：教学源、图源、代码和报告的逐文件映射。

可运行代码和实际报告位于 `examples/lesson19/`。本讲没有外部或生成的位图插图，不存在用图片查询词冒充原图的问题。正文内的图是可在 GitHub 与聊天中渲染的 Mermaid 源。

## 如何核验

从 GitHub 读回每个清单文件，按 UTF-8 字节计算 SHA-256，与 `source-manifest.json` 对照。将 `transcript.md` 的引用 token 按 `citation-map.json` 逆向替换，再与教学文件去除末尾引用定义后的内容比较，应完全一致。代码的报告与主代理复跑输出已经比较一致。

最终 GitHub 发布后另保存 `delivery-verification.json`，记录实际内容提交号、远端读回与字节比较结果。该验证证明上传内容与保留源一致；不声称已经从平台导出并比对最终聊天 UI。

后续技术勘误应新增说明，不直接覆盖已留存的原授课文本。历史第 1–18 讲的原文和原始图片恢复仍另行跟踪，第 13、17 讲缺文件状态不得因此被改为已恢复。
