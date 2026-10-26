# MGGA 证据与裁决标准 / Evidence and Editorial Policy

## 目的 / Scope

MGGA 记录游戏开发、发行、第三方咨询、官方推广和已公开的玩家互动争议。项目**不评价游戏品质**。涉及 DEI 的政策表述可以作为一项独立事实被记录，但 DEI 并不是某个特定公司、单一组织，也不自动代表不当行为；一款游戏出现不同背景的角色，不能推出存在咨询合作关系。对于具体制作参与，需直接证据。

The archive records specific, publicly verifiable corporate/production conduct and related disputes, not a game's artistic or technical quality. Narrative tropes or the existence of DEI statements alone do not establish third-party production involvement or misconduct.

## 证据等级 / Evidence tiers

| 层级 | 中文 | English | 可用于正式名单? |
|:---|:---|:---|:---:|
| L0 | 搜索结果、标题、匿名投稿 | Search hits / anonymous submissions | 否 |
| L1 | 可定位原帖，但仅能证明“有人作出该说法” | Original post documenting an allegation | 否 |
| L2 | 游戏制作署名、工作室公开合作名单、正式声明、完整原始录音及具可核实上下文的公开材料 | Direct credits, source announcement, documented public facts | 在经人工复核后可以 |
| L3 | 两个互相独立的直接来源或一份高可信原始材料结合反证检查 | Cross-checks, independent primary evidence and rebuttal review | 优先 |

**核实关系 ≠ 裁决加入避购**。L2/L3 证明的只能是证据实际支持的具体命题，不可夸大含义；名单是维护者个人的避购选择，不是法律裁决。

## 游戏状态 / Independent fields

- `investigation_status`: `unreviewed`、`investigating`、`verified_link`、`disputed`、`no_verified_link`。未检索到可核实证据只代表本轮未找到。
- `decision`: `pending`、`listed`、`remediated`、`not_listed`。只有维护者审核后人工更改，任何抓取程序都不得填写或自动修改。
- `issues[]`: 每项事实独立写中英标题，并通过 `evidence_ids[]` 指向至少一条经复核的证据。
- `evidence.*`: 每条均需 `id`、`file`、`source_url`、`verification_status`、`checked_at`，保存 Markdown 文件记录原文出处、证据限制、采集时点和反证。
- `remediation`: 如果有充分证据证明公开更正、道歉、具体人员已离任或制作关系解除及补救，应记录 `completed`、日期、中英说明和原始链接。**员工离职不自动证明其先前参与内容已经被移除**。

## 精确示例 / Example of a verified evidence entry

```json
{
  "id": "case-001-promo-01",
  "file": "附加材料 (Supplementary Materials)/证据 (Evidence)/宣发材料 (Promotional Materials)/case-001/official-statement.md",
  "source_url": "https://example.org/original-statement",
  "verification_status": "verified",
  "checked_at": "2026-10-26"
}
```

> 上例 URL 仅是 schema 示例，**不是证据**，不可照抄作为真实游戏的关联证明。

## 原始证据保存与版权

证据 Markdown 推荐记录：游戏名/ID、具体命题、官方或源头 URL、截图拍摄时间（UTC+8）、原始发布日期、保存人、原文短摘录、上下文、验证步骤、反证及疑问。对拥有版权许可的截图/视频可存本仓库；第三方文章优先保存链接、摘要和小范围必要引用，不整篇复制。禁止记录住址、私人联系方式、未经授权私信、凭据、仇恨攻击和骚扰号召。

## 更正、申诉和删除线 / Corrections and remediation

- 保存所有原记录及时间。新证据反驳旧结论时，应通过 Git commit 和对应材料页注明更正缘由。
- 维护者人工将 `decision` 从 `listed` 改为 `remediated`，记录具体日期和补救来源；首页以 ~~删除线~~ 形式保留该条历史。
- `remediated` 不是本项目当前避购名单，仍显示在“历史留档”。与事实错误导致撤回的情况也应清晰区分，不把虚假指控作为历史事实继续传播。
- 可通过 GitHub Issue 提交反证或要求纠正具体事实。
