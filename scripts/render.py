"""Render bilingual README indices, report links and GitHub Pages search JSON."""
from __future__ import annotations
from collections import defaultdict
from datetime import datetime
from html import escape as html_escape
from common import ROOT, evidence_path, load_json, save_json, rel_url, md_safe
from validate import check

DECISION_LABELS = {
  'pending':('待裁决','Pending'), 'listed':('已列入','Listed'),
  'remediated':('已补救 · 历史保留','Remediated · archived'),
  'not_listed':('未列入','Not listed'),
}
CATEGORIES=[('reviews','测评','Reviews'),('promotional','宣发材料','Promotional'),('player','玩家证据','Player evidence'),('remediation','补救时间线','Remediation')]

def row(g,lang):
    zh=lang=='zh'
    title=f"[{md_safe(g['title_en'])}]({g['official_url']})"
    if g['decision']=='remediated': title=f'~~{title}~~'
    date=(f"{g['release_date'][:4]}年{int(g['release_date'][5:7])}月" if zh else g['release_date'][:7])
    platforms=' / '.join(md_safe(x) for x in g['platforms'])
    cn=md_safe(g['title_zh'])
    primary=f'**{title}**（{cn}） · {date} · {platforms}' if zh else f'**{title}** ({cn}) · {date} · {platforms}'
    issues='；'.join(md_safe(i['title_zh']) for i in g['issues']) if zh else '; '.join(md_safe(i['title_en']) for i in g['issues'])
    links=' · '.join(f'[{cnlab if zh else enlab}]({rel_url(evidence_path(kind,g["game_id"]))})' for kind,cnlab,enlab in CATEGORIES)
    lab='涉及事项' if zh else 'Documented issue'
    correction=(' **｜已补救，保留历史记录**' if zh else ' **| Remediated; history retained**') if g['decision']=='remediated' else ''
    return f'- {primary}\n  - **{lab}：** {issues}{correction} · {links}\n'

def list_section(games,lang):
    listed=[g for g in games if g['decision'] in {'listed','remediated'}]
    listed.sort(key=lambda g:(g['title_en'].casefold(),g['game_id']))
    groups=defaultdict(list)
    for g in listed:
        initial=g['title_en'].lstrip().upper()[:1]
        groups[initial if 'A'<=initial<='Z' else '#'].append(g)
    if not listed:
        return ('> **暂无经过完整核验并完成裁决的条目。** 搜索线索不自动成为指控或黑名单。\n'
                if lang=='zh' else '> **No cases have passed evidence verification and editorial listing review yet.** Search leads are not allegations.\n')
    letters=sorted(groups,key=lambda s:(s=='#',s))
    nav='　'.join(f'[{x}](#letter-{x.lower() if x!="#" else "other"})' for x in letters)
    chunks=[nav,'']
    for letter in letters:
        anchor=letter.lower() if letter!='#' else 'other'
        chunks.extend([f'<a id="letter-{anchor}"></a>',f'### {letter}',''])
        chunks.extend(row(g,lang) for g in groups[letter])
    return '\n'.join(chunks)

def render_one(template_name,out_name,lang,games,state):
    src=(ROOT/'templates'/template_name).read_text(encoding='utf-8')
    listings=list_section(games,lang)
    catalog_count=len(games)
    listed=sum(g['decision']=='listed' for g in games)
    remed=sum(g['decision']=='remediated' for g in games)
    lead_count=state.get('total_leads',0)
    status=(f'已建档 **{catalog_count}** · 当前避购 **{listed}** · 历史补救 **{remed}** · 待核查新闻线索 **{lead_count}**'
            if lang=='zh' else f'Catalog **{catalog_count}** · Active avoid list **{listed}** · Remediated archives **{remed}** · Unverified news leads **{lead_count}**')
    updated=state.get('last_published_at') or ('尚未自动发布' if lang=='zh' else 'Not published yet')
    example=next((g for g in games if g['decision']=='pending' and not g['issues']),None)
    if example:
        label=('**信息登记示例（不代表黑名单指控）**' if lang=='zh' else '**Catalog example (NOT a blacklist allegation)**')
        links=' · '.join(f'[{c if lang=="zh" else e}]({rel_url(evidence_path(kind,example["game_id"]))})' for kind,c,e in CATEGORIES)
        sample=f'{label}\n\n**{md_safe(example["title_en"])}**（{md_safe(example["title_zh"])}） · {example["release_date"]} · {" / ".join(md_safe(p) for p in example["platforms"])}\n\n- **{"参与活动" if lang=="zh" else "Documented issue"}：** {"暂无经证实事项；不列入避购清单" if lang=="zh" else "None verified; not included in avoid list"} · {links}\n'
    else: sample=''
    src=src.replace('<!-- MGGA-COUNTS -->',status).replace('<!-- MGGA-INDEX -->',listings).replace('<!-- MGGA-SAMPLE -->',sample).replace('<!-- MGGA-UPDATE -->',updated)
    (ROOT/out_name).write_text(src,encoding='utf-8')

def main():
    games=load_json('data/games.json')
    errs=check(games)
    if errs: raise SystemExit('\n'.join(errs))
    state=load_json('data/monitor_state.json')
    render_one('README.zh.md','README.md','zh',games,state)
    render_one('README.en.md','README.en.md','en',games,state)
    data=[]
    for g in sorted(games,key=lambda v:v['title_en'].casefold()):
        data.append({
            'id':g['game_id'],'en':g['title_en'],'zh':g['title_zh'],
            'aliases':g.get('aliases_zh',[]),'platforms':g['platforms'],
            'date':g['release_date'],'decision':g['decision'],
            'investigation_status':g['investigation_status'],
            'issues_zh':[x['title_zh'] for x in g['issues']],
            'issues_en':[x['title_en'] for x in g['issues']],
            'evidence':{kind: '../'+rel_url(evidence_path(kind,g['game_id'])) for kind,_,_ in CATEGORIES},
            'official':g['official_url'],
        })
    # Site links point to GitHub repository files, not non-existent relative Pages assets.
    for item in data:
        for kind in item['evidence']:
            item['evidence'][kind]='https://github.com/GGforceP/MGGA/blob/main/'+item['evidence'][kind][3:]
    save_json('docs/search-index.json',data)
    # Read-only public feed for search; no unverified leads in verified list.
    print(f'Rendered {len(games)} games, {sum(g["decision"]=="listed" for g in games)} listed.')
if __name__=='__main__': main()
