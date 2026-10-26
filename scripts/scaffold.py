"""Create four game-specific evidence folders without overwriting existing files."""
from common import ROOT, CATEGORIES, SUPP, load_json, evidence_path

LABELS = {
  "reviews": "测评 / Reviews",
  "promotional": "宣发材料 / Promotional materials",
  "player": "玩家提交证据 / Player-submitted evidence",
  "remediation": "补救方式、时间 / Remediation timeline",
}

def run():
    for game in load_json('data/games.json'):
        for kind in CATEGORIES:
            p=ROOT/evidence_path(kind, game['game_id'])
            p.parent.mkdir(parents=True, exist_ok=True)
            if not p.exists():
                p.write_text(
                    f"# {game['title_en']} — {LABELS[kind]}\n\n"
                    "**状态 / Status：尚未提交经核实的此类证据 / No verified material filed in this category.**\n\n"
                    "提交时需包含：具体命题、原始来源链接、公开发布日期、截取时间、上下文、反证检查、文件授权状态。\n\n"
                    "Required: precise claim, primary source URL, publication date, capture date, context, counter-evidence check, and file rights.\n\n"
                    "不得把新闻搜索结果或个人主观感受自动认定为某组织实际参与制作。\n",
                    encoding='utf-8'
                )
if __name__ == '__main__':
    run()
