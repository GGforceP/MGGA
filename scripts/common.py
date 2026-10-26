"""Shared MGGA path and JSON helpers (stdlib only)."""
from __future__ import annotations
import json
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
SUPP = "附加材料 (Supplementary Materials)"
CATEGORIES = {
    "reviews": "证据 (Evidence)/测评 (Reviews)",
    "promotional": "证据 (Evidence)/宣发材料 (Promotional Materials)",
    "player": "证据 (Evidence)/玩家搜集到的证据 (Player-Submitted Evidence)",
    "remediation": "补救方式、时间 (Remediation & Timeline)",
}

def load_json(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))

def save_json(rel, value):
    p=ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def evidence_path(kind, game_id):
    return f"{SUPP}/{CATEGORIES[kind]}/{game_id}/README.md"

def rel_url(path):
    return quote(path, safe="/-._~")

def md_safe(s):
    return str(s).replace('\\', '\\\\').replace('|', '\\|').replace('[', '\\[').replace(']', '\\]').replace('\n',' ')
