# MGGA 目录结构 / Repository Structure

```text
MGGA/
├── README.md                                   # 中文首页（自动生成）
├── README.en.md                                # English homepage (generated)
├── EVIDENCE_POLICY.md                         # 证据与裁决标准
├── CONTRIBUTING.md                            # 贡献/录入/核验流程
├── ROADMAP.md                                 # 全平台覆盖扩展路线
├── PROJECT_STRUCTURE.md                       # 当前仓库结构与用途
├── DEPLOY.md                                  # 首次部署与测试指引
├── 附加材料 (Supplementary Materials)/
│   ├── 证据 (Evidence)/
│   │   ├── 测评 (Reviews)/
│   │   │   └── <game_id>/README.md            # 单款游戏测评/相关附件
│   │   ├── 宣发材料 (Promotional Materials)/
│   │   │   └── <game_id>/README.md            # 官方推广/公开声明/图片
│   │   └── 玩家搜集到的证据 (Player-Submitted Evidence)/
│   │       └── <game_id>/README.md            # 来源、截图及复核结论
│   └── 补救方式、时间 (Remediation & Timeline)/
│       └── <game_id>/README.md                # 道歉/更正/解除合作等时间线
├── templates/
│   ├── README.zh.md                            # 中文生成源
│   ├── README.en.md                            # English source
│   └── EVIDENCE_RECORD.md                     # 新增证据模板
├── research/
│   ├── README.md                             # 中文独立调查登记册（非黑名单）
│   ├── README.en.md                          # English research registry
│   └── cases/<game_id>.md                    # 独立游戏调查档案 100 个
├── data/
│   ├── intake-2026-10-26.json               # 本轮采集依据
│   ├── games.json                              # 人工核准资料及避购裁决
│   ├── leads.json                              # 自动采集的未核查新闻线索
│   ├── monitor_queries.json                    # 多语言 RSS 检索配置
│   └── monitor_state.json                      # 自动发布状态与统计
├── reports/
│   ├── initial-100-2026-10-26.md            # 初始100款入库报告
│   └── latest.md                               # 最近采集报告
├── docs/
│   ├── index.html                              # GitHub Pages 可搜索页面
│   └── search-index.json                      # 页面搜索数据（自动生成）
├── scripts/
│   ├── common.py
│   ├── scaffold.py
│   ├── validate.py
│   ├── render.py
│   ├── collect.py
│   ├── publish.py
│   └── get_scan_run.py
├── tests/
│   └── test_mgga.py
└── .github/
    ├── workflows/
    │   ├── collect.yml                         # UTC+8 02:00
    │   ├── publish.yml                         # UTC+8 06:00
    │   └── check.yml                           # PR 验证
    └── ISSUE_TEMPLATE/
        └── evidence-report.yml
```

`<game_id>` 是 `data/games.json` 中的稳定标识符。每次新增游戏，应运行 `python scripts/scaffold.py` 生成四类材料目录。因为 Git 不追踪空目录，需要保存 `README.md` 等文件作为入口；资料可根据来源分类继续新增。每次新增/重命名目录，**同步修改本文件及中英 README 的结构引用**。

本轮新增 100 个游戏资料文件与四类合计 400 个材料目录，每个目录保存 README 供证据继续补充。

**发布隔离规则：** `README.md`、`README.en.md` 和 `docs/search-index.json` 只允许经证据审核和人工批准的 `listed/remediated` 条目；`pending/not_listed` 只列在 `research/README.md` 和 `research/README.en.md`。每天的自动渲染必须维持此边界。
