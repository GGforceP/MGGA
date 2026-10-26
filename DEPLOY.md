# MGGA 首次部署（目标：GGforceP/MGGA）

## 1. 建立空仓库

在已登录 `GGforceP` 的浏览器打开 <https://github.com/new>，名称填写 `MGGA`，建议设为 `Public`，**不要勾选 Initialize with README、.gitignore 或 License**（本模板已含 README/.gitignore）。

## 2. Windows PowerShell 一次上传

先在本地安装 Git for Windows，将压缩包解压到任意位置，然后进入解压后的 `MGGA` 文件夹打开 PowerShell：

```powershell
git init
git branch -M main
git remote add origin https://github.com/GGforceP/MGGA.git
git add .
git commit -m "Initialize MGGA bilingual evidence archive"
git push -u origin main
```

如已有同名仓库，先检查仓库文件，勿直接强制覆盖。以上命令要求 Git 的身份凭证已正确登录。

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
