# MGGA 贡献与维护 / Contributing

## 新增游戏 / Add a game

1. 到发行商/平台官方资料确定英文标题、简体中文官方名称、发布日期及平台；给出官方来源 URL。
2. 在 `data/games.json` 添加稳定唯一 `game_id`、中英名称与别名，初始 `investigation_status=unreviewed`、`decision=pending`、空 `issues/evidence`。
3. 运行 `python scripts/scaffold.py`，为这款游戏创建四类证据子目录，再使用 `templates/EVIDENCE_RECORD.md` 记录命题，把证据 Markdown、**有权存储**的截图或文件放入对应目录。
4. 对可核实的证据记录 `id`、`file`、`source_url`、`checked_at`、`verification_status=verified`，写明确切命题和反证检查；把证据 id 关联到 `issues[].evidence_ids`。
5. **默认留在 [独立调查登记册](research/README.md)，不得直接出现在正式 README。** 经过复核后，选择 `review_basis=verified_conduct`（已证实具体事项、`investigation_status=verified_link`）或 `review_basis=documented_player_controversy`（三个以上经核验独立玩家来源、两个以上域名，`investigation_status=disputed`，并明确标明 `issues[].claim_status=disputed`）。所有条目都必须有经过核验的 `issues[].evidence_ids`。
6. **仅在维护者明确批准后** 填写 `editorial_approval: {"status":"approved","reviewed_by":"maintainer","reviewed_at":"YYYY-MM-DD"}` 并设 `decision=listed`。自动采集程序永远无权设置此字段。大量玩家争议只能证明争议存在，不等于争议中的指控属实。
7. 整改成功，填写 `remediation` 的 `status=completed`、ISO 日期、中英说明与官方可访问 URL，并人工把 `decision=remediated`。如只是主张错误，公开更正而非继续展示为事实。
8. `python scripts/validate.py && python scripts/render.py && python -m unittest discover -s tests -v`，PR 中附相关材料。

自动搜集程序不改动 `data/games.json`。所有行为需通过 git 历史追溯。

## 双语 README / Bilingual READMEs

README **只显示经证据核验并获人工审核批准的正式记录**。待调查的游戏另存于 `research/README.md` 和 `research/README.en.md`，页面和公开搜索索引不展示待查游戏。README 的长期编辑源位于 `templates/README.zh.md` 和 `templates/README.en.md`；其中 `<!-- MGGA-INDEX -->`、`<!-- MGGA-COUNTS -->` 由 `scripts/render.py` 生成。**不要只修改生成的 `README.md` 或 `README.en.md`**；发布阶段会覆盖。

## 搜索页面 / Search

仅从已经批准列入的正式条目自动生成 `docs/search-index.json`，`docs/index.html` 使用本地 JavaScript 读取。GitHub README 禁止运行 JavaScript，因此只有在仓库 Settings → Pages → Deploy from a branch → `main` → `/docs` 启用 Pages 之后，`https://GGforceP.github.io/MGGA/` 才提供交互式搜索。

## 定时运行 / Schedules

`collect.yml` 02:00 UTC+8 采集并暂存同一天的 `mgga-scan` workflow artifact（不 commit）；`publish.yml` 06:00 UTC+8 从成功完成的当天采集 run 下载该 artifact，合并发布。两次 Actions schedule 均设置 `timezone: Asia/Shanghai`。

首次手动验证：从 Actions 手动运行 `MGGA Collect at 02 UTC+8`，等待成功后再运行 `MGGA Publish at 06 UTC+8`。无同日成功 artifact 或所有 RSS 全失败时，发布工作流应失败而不是覆盖现有数据。

GitHub Scheduled Actions 会排队延迟或跳过。频繁提交本身不等于保证仓库每天准点成功发布，建议在 Actions 中检查失败通知；若需严格 SLA，请改用外部调度器并配置失败重试。
