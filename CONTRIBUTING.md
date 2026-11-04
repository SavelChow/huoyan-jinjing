# 小组协作与 PR

## 分支和目录

成员分支使用 `memberNN/任务`，如 `member06/resnet-baseline`，只修改对应 `members/member06_research/`。一项交付一个 PR；PR 合并后从最新 main 开新分支。
公共文件、跨模块集成由仓库所有者使用 `integration/任务` 分支提交。公共变更需解释影响，并让相关负责人确认。

尚未收集成员 GitHub 用户名：不自动邀请协作者，也不假定账号身份。成员 Fork 后即可开 PR。分支目录检查只验证改动范围，不是身份认证；组长应人工确认提交者角色。CODEOWNERS 统一请求组长审核。

## 示例（成员 4）

```bash
git clone https://github.com/YOUR_USERNAME/huoyan-jinjing.git
cd huoyan-jinjing
git remote add upstream https://github.com/ZhenyuXu0724/huoyan-jinjing.git
git fetch upstream
git switch -c member04/hog-baseline upstream/main
# 只修改 members/member04_hog/
git add members/member04_hog
git commit -m "feat(member04): add HOG baseline"
git push -u origin member04/hog-baseline
```

在 GitHub 向上游 main 创建 PR。`YOUR_USERNAME` 替换为自己的账号。

## 每次交付

- 更新自己目录 README 的运行命令、依赖、输出、限制与交接记录。
- 更新 progress.md：未开始/进行中/待审核/完成，填写提交或实验 ID。
- 给出最小复现输入、输出格式、验证命令和结果；不得上传测试真值来辅助推理。
- 模型权重用有权限的外部存储或 Releases 交付，在 README 写版本、SHA256 和访问方式。
- 未实现的接口应显式报错，不能用随机/空预测冒充成功。

## 自动检查

- 结构、固定类别和模型注册；基本接口测试。
- PR 范围：memberNN 分支只允许自己的目录；integration 分支只允许仓库所有者发起。
- PR 禁止原始媒体、模型权重、封存真值/个人材料和超 5 MiB 文件进入 Git。

检查用于发现问题，不替代组长审查；.gitignore 也不是信息保密或权限控制。工作流在普通 pull_request 事件运行，使用只读权限；首次 Fork 工作流可能需要组长在 GitHub 批准运行。

## 合并标准

目录符合职责、检查通过、运行说明完整、证据真实、组长批准。测试前先冻结配置；独立测试后变更记录版本与数据已接触事实。不要把尚未通过实际验收的任务标为完成。
