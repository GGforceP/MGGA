<div align="center">
<h1>MGGA · Make Games Great Again</h1>
<p><strong>全球游戏争议与公开证据档案 / Global Game Accountability Archive</strong></p>
<p><strong><a href="README.md">简体中文</a>　｜　<a href="README.en.md">English</a></strong></p>
<p><sub>关注发行、制作合作、官方言论与玩家争议；不评价游戏品质。所有重要结论均可追溯、可复核、可更正。</sub></p>
</div>

---

### 项目概览

<!-- MGGA-COUNTS -->

**[A–Z 正式列表](#mgga-list)**　·　**[游戏搜索](https://GGforceP.github.io/MGGA/)**（需启用 GitHub Pages）　·　**[最新采集报告](reports/latest.md)**　·　**[提交线索](.github/ISSUE_TEMPLATE/evidence-report.yml)**　·　**[英文版](README.en.md)**

> **三层独立判断**：新闻或社区**线索** → 原始材料证明的**具体事实** → 用户的**避购裁决**。以上三者不是同一件事。项目会记录有争议的官方政策、公开言论、已证明的顾问合作与玩家争议，但不会把 DEI 这个概念本身等同于不当行为，也不会把传闻自动升级为事实。

<a id="mgga-list"></a>

### 正式避购名单 · A–Z

按**官方英文游戏名**首字母排序；每款游戏下一行是具体事项和证据入口。发行平台及时间不属于违规证据。已核实整改的记录采用 ~~删除线~~ 保留历史，不从档案中删除。

<!-- MGGA-INDEX -->

### 首批100款热门游戏 · A–Z调查目录

> **以下是调查目录，不是黑名单。** 已建立 75 款 Steam 热门游戏与 25 款跨平台热门作品档案；具体纠纷、官方大陆译名、版本发行日期仍需独立核查。所有已核实和未核实的线索须分开。

[100款调查报告](reports/initial-100-2026-10-26.md) · [入库来源记录](data/intake-2026-10-26.json) · [可搜索页面](https://GGforceP.github.io/MGGA/)

<!-- MGGA-CATALOG -->

### 资料入口

| 分类 | 用途 |
|:---|:---|
| [测评 / Reviews](附加材料%20%28Supplementary%20Materials%29/证据%20%28Evidence%29/测评%20%28Reviews%29/) | 可验证的游戏内容、媒体测评与完整上下文 |
| [宣发材料 / Promotional Materials](附加材料%20%28Supplementary%20Materials%29/证据%20%28Evidence%29/宣发材料%20%28Promotional%20Materials%29/) | 开发商、发行商、官方发布渠道的原始文字及公开档案 |
| [玩家提交 / Player-Submitted](附加材料%20%28Supplementary%20Materials%29/证据%20%28Evidence%29/玩家搜集到的证据%20%28Player-Submitted%20Evidence%29/) | 待复核图片、片段、截图、讨论来源与时间戳 |
| [补救时间线 / Remediation](附加材料%20%28Supplementary%20Materials%29/补救方式、时间%20%28Remediation%20%26%20Timeline%29/) | 道歉、纠正、撤回、人员离任及相关官方证据 |

### 自动维护

| 时段（北京时间 UTC+8） | 工作 | 正式名单是否自动变化 |
|:---|:---|:---|
| 每日 **02:00** | 采集多语言公开 RSS/新闻检索结果并暂存 Actions artifact，去重与生成未核验线索 | 否 |
| 每日 **06:00** | 校验当天采集结果，更新线索、统计、双语首页和可搜索索引并提交到 `main` | 仅刷新展示；**不自动裁决** |

上次成功发布：**<!-- MGGA-UPDATE -->**。GitHub Actions 整点定时属于尽力调度，可能延迟或丢弃；不承诺精确到分秒。首次部署需手动触发 `collect` 再触发 `publish`，并在 Settings → Pages 启用 `docs/` 搜索网页。

### 证据与收录规则

1. 收录公开可核验的具体行为，不根据角色设定、人物身份、孤立关键词或未经核实的传闻推定商业合作。
2. 每项已核实的结论必须具备**原始来源、具体命题、日期、文件、复核记录**；截图需保留上下文，不应侵犯版权、隐私或鼓励骚扰。
3. **补救、反证、更正与撤回**保留历史和时间；删除线代表裁决变更，不代表原事实被抹去。
4. `data/games.json` 的 `decision` 是人工维护；自动采集只更新 `data/leads.json`。未检索到线索不等于证实不存在关联。

相关文档：[证据标准](EVIDENCE_POLICY.md) · [维护说明](CONTRIBUTING.md) · [全球覆盖路线图](ROADMAP.md) · [完整目录](PROJECT_STRUCTURE.md)。
