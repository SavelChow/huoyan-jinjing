# 公共接口 v0.1

这是集成起点。变更须由组长审核同步，正式训练前冻结实际版本。

## 模型入口

四个模型模块均提供 `predict(image_path: str) -> dict`。模型加载、权重路径和配置由模块维护；不要在导入模块时自动下载或开始训练。
图像分类器返回：`status`, `predicted_label`（PASS/FAIL 或 null）, `prediction_score`（数值或 null）, `score_type`。实际支持的固定数量在模块配置记录；统一入口检查不支持的数量，返回 UNSUPPORTED_COUNTS 和 null 判定/得分。
对象模型返回：`status`, `objects`（列表）；每项含 `class_id`, `bbox: [xmin,ymin,xmax,ymax]`, `score`。框采用原始图像像素、左上角原点、连续半开区间 [xmin,xmax)×[ymin,ymax)，边界限定在图像内。计数由同一最终保留对象列表派生。拒绝标签为 0。

对象模型不得接收 expected_counts 或 GT；用户改变要求不得改变框/类别/数量。统一决策层将实际计数与合法 expected_counts 比较，且 non_catalogue 固定预期为零。检测分数未经校准时明确标为未校准分数；规则判定图像分数为 null，不能虚构概率。

## 状态与失败

建议状态：OK、REVIEW_REQUIRED、UNSUPPORTED_COUNTS、INPUT_ERROR、NOT_IMPLEMENTED。需复核或失败时 predicted_label/prediction_score 为 null，单独报告覆盖率，不能作为 PASS。已检出目录外的有效对象级结果必须 FAIL。
当前模型与批量导出尚未实现，显式抛出 NotImplementedError。空 objects 只有在实际完成推理且确实无检测时才合法，不能作为占位结果。

## 批量输入

`python predict.py --input_dir DIR --model MODEL_ID --output_dir DIR --counts_file FILE`
counts_file 是列表，每项只有 image_id（图像文件名）和 expected_counts（字符串键 1–5，非负整数，不能是 bool）。同次运行文件名唯一，不含真实数量、框或正确答案。相同图像不同预期数量分开运行。

## 输出文件

| 文件 | 字段/内容 |
|---|---|
| images.csv | image_id, model_id, status, predicted_label, prediction_score, score_type, non_catalogue_count |
| objects.csv | image_id, model_id, detection_id, class_id, xmin, ymin, xmax, ymax, score |
| counts.csv | image_id, class_id, observed_count, expected_count, difference（observed-expected），包含 ID 0–5 |
| run_config.json | 模型版本、类别表、预处理、阈值、拒绝/标定/容差、坐标约定、分数含义、硬件、能力标记、逐图输入预期数量；固定数量模型另记支持规则 |

图像分类器只交 images.csv、run_config.json，不伪造对象与计数。对象系统必须交全部文件。真实标注由成员 3 独立管理，推理不得读取。

## 接口验收

模型负责人提供最小命令、配置、依赖、样例、分数含义和失败状态；成员 7 接入路由/导出，组长验收。评价器使用共同 IoU≥0.50 一对一规则，忽略对象处理和 tie-break 需明确并固定。
