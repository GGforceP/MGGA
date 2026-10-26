# MGGA 首次部署（目标：GGforceP/MGGA）

## 1. 当前仓库已推送（2026-10-26）

GitHub 仓库已建立：[GGforceP/MGGA](https://github.com/GGforceP/MGGA)。首次100款调查档案和证据分类目录现已上传，无需重新创建空仓库，也不需要强制推送。

## 2. 首批100款档案

- [中文主页](README.md) / [English](README.en.md)
- [首批调查报告](reports/initial-100-2026-10-26.md)
- [100条游戏主数据](data/games.json) 与 [入库来源快照](data/intake-2026-10-26.json)
- [调查档案目录](research/cases/)

## 3. 启用与验证自动任务

1. GitHub 仓库 **Settings → Actions → General**：检查 Actions 工作流执行权限；发布需要 `GITHUB_TOKEN` 对 contents 的写入权限（工作流内已声明 `permissions: contents: write`，可能受组织策略限制）。
2. 打开仓库 **Actions → MGGA Collect at 02 UTC+8 → Run workflow**，确认上传临时 artifact；再运行 **MGGA Publish at 06 UTC+8 → Run workflow**，确认 `reports/latest.md` 更新。
3. **Settings → Pages → Build and deployment → Deploy from a branch → `main` + `/docs`**，保存；完成后交互搜索地址是 <https://GGforceP.github.io/MGGA/>。
4. 工作流默认使用 GitHub 免费公开 RSS 检索，**无需添加 token 或开放订阅私链**。真实检索可能受到网络环境、RSS 提供方限制。
5. GitHub 任务有队列延迟；02:00、06:00 是**计划触发时点**，不是准时完成保证。观察 Actions 的失败日志，必要时手动补发。

## 4. 项目维护入口

- 正式核实/裁决：`data/games.json`，具体格式与字段见 `CONTRIBUTING.md`。
- 证据材料：`附加材料 (Supplementary Materials)/`，四个独立证据区。
- 多语言检索：`data/monitor_queries.json`。
- 双语首页说明：`templates/README.zh.md` 和 `templates/README.en.md`，运行 `python scripts/render.py` 更新。
- 校验：`python scripts/validate.py`；回归测试：`python -m unittest discover -s tests -v`。
