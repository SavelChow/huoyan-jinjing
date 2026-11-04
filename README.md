# 火眼金睛

机械零件视觉检测课程项目：五类规定规格识别、数量核验和目录外零件定位拒绝。

**当前状态：交付框架已建立，模型尚未实现。** 不输出虚构检测或实验成绩。
仓库地址采用拼音 `huoyan-jinjing`（GitHub 不支持中文仓库路径）。

## 找到自己的目录

| 人员 | 目录 | 主责 |
|---|---|---|
| 组长 | [member01_lead](members/member01_lead/) | 需求、集成、冻结、研究决策与报告统稿 |
| 成员 2 | [member02_setup](members/member02_setup/) | 装置、标定与采集组织 |
| 成员 3 | [member03_data](members/member03_data/) | 公开数据审查、标注、划分与真值质检 |
| 成员 4 | [member04_hog](members/member04_hog/) | HOG+MLP、统一图像级评价 |
| 成员 5 | [member05_detector](members/member05_detector/) | YOLO、基础拒绝、对象与计数评价 |
| 成员 6 | [member06_research](members/member06_research/) | 冻结 ResNet18 基线、研究改进和消融 |
| 成员 7 | [member07_app](members/member07_app/) | 摄像头/UI、统一入口、导出、端到端计时 |

每人只需维护自己的目录：`README.md` 写交付和运行说明，`progress.md` 跟踪个人时间线，代码直接放目录内，需要时再拆子目录。交接与个人贡献写在 README 中，不再重复建立多个模板。

## 最短上手路径

```bash
git clone https://github.com/ZhenyuXu0724/huoyan-jinjing.git
cd huoyan-jinjing
python -m venv .venv
# 激活虚拟环境后，按需要安装本模块依赖
python predict.py --list-models
python -m unittest discover -s tests -v
```

Python 基准版本为 3.11；框架检查只使用标准库。模型依赖由各成员在自己目录的 requirements.txt 提报，组长统一锁定根目录环境，勿一次安装所有框架。

## 如何交付

1. Fork 本公开仓库到自己的账号（无需先获得写权限）。
2. 从最新 main 建任务分支，例如 `member04/hog-baseline`。
3. 只改 `members/member04_hog/`，更新交付说明和进度。
4. 向本仓库 main 发 PR；按模板写运行方式、证据和未完成项。
5. 组长审核后合并。公共接口需要变更时，在 PR 中提出，由组长用 `integration/主题` 分支整合。

详见 [CONTRIBUTING.md](CONTRIBUTING.md)。目录是协作边界，不是 GitHub 的文件夹写权限。账号认领未完成前，CI 依据分支名检查目录；主分支规则若启用，则组长审批与检查为合并条件。

## 公共约定

- [接口和输出格式](shared/CONTRACT.md)
- [类别与模型注册表](shared/catalogue.json)
- [数量文件示例](shared/expected_counts.example.json)
- [全组计划与提交节点](members/member01_lead/PLAN.md)
- [大文件与数据版本说明](artifacts/README.md)

仓库只保存可公开的代码、配置、文档与小型结果。封存测试集及其真值、个人信息、密钥、原始大批图片和权重不入 Git。

## 课程批量入口

```bash
python predict.py --input_dir ./data/images --model baseline3 --output_dir ./outputs/run01 --counts_file ./expected_counts.json
```

该入口已建立路由，尚未实现的模型和导出会明确报错并非零退出；真实推理由成员 4/5/6 实现，批量导出由成员 7 完成。四个模型 ID：baseline1、baseline2、baseline3、final。

项目公开不代表第三方数据/权重获得再分发授权。外部来源与许可须在模块 README 记录；本仓库暂不预设全组代码的开源许可证。
