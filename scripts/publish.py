"""06:00 Asia/Shanghai: publish 02:00 scan to repo, without auto-listing titles."""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from common import ROOT, load_json, save_json

TZ=ZoneInfo('Asia/Shanghai')

def merge(existing,incoming,max_total=1500):
    indexed={x['id']:dict(x) for x in existing}
    new=0
    for x in incoming:
        if x['id'] in indexed:
            old=indexed[x['id']]
            old['matched_queries']=sorted(set(old.get('matched_queries',[]))|set(x['matched_queries']))
            old['languages']=sorted(set(old.get('languages',[]))|set(x['languages']))
            old['facets']=sorted(set(old.get('facets',[]))|set(x.get('facets',[])))
            old['last_seen_at']=x['first_seen_at']
        else:
            indexed[x['id']]=dict(x)
            indexed[x['id']]['last_seen_at']=x['first_seen_at']
            new+=1
    all_rows=sorted(indexed.values(),key=lambda x:(x.get('last_seen_at') or '',x['id']),reverse=True)
    return all_rows[:max_total],new

def make_report(scan,total):
    lines=["# MGGA 每日公开线索报告 / Daily Unverified Discovery Report",'',
           f"**采集日期（UTC+8）/ Scan date**：{scan['collected_on']}",
           f"**本次发现 / Leads in scan**：{len(scan['leads'])} · **去重保留 / Retained**：{total}",
           f"**失败查询 / Failed feeds**：{len(scan['failed_queries'])}/{scan['queries_executed']}",'',
           '> **重要：以下仅是搜索标题与聚合链接，未经核实。不构成对任何游戏、员工、工作室或组织的事实指控；不自动进入黑名单。**',
           '> **Important: Unverified headlines and aggregation links only; not allegations, proof of a relationship, or an avoid-list verdict.**','']
    if scan['failed_queries']:
        lines+=['## 查询异常 / Feed errors','']
        for err in scan['failed_queries']:
            lines.append(f"- `{err['query']}`：{err['error'][:160].replace(chr(10),' ')}")
        lines.append('')
    lines+=['## 本次采集 / Latest scan','']
    for lead in scan['leads']:
        # Headline is untrusted RSS content. Escape Markdown to avoid unintended links or rendering.
        title=lead['headline'].replace('\\','\\\\').replace('[','\\[').replace(']','\\]').replace('|','\\|').replace('\n',' ')
        src=lead['source_name'].replace('|','\\|').replace('\n',' ')
        u=lead['aggregator_url']
        if not u.startswith('https://'):continue
        lines.append(f"- [{title}](<{u}>) — {src} · {lead.get('published_at') or 'date unknown'} · `unverified` · {', '.join(lead.get('facets',[]))}")
    if not scan['leads']: lines.append('- 当前无新线索 / No leads captured.')
    lines+=['','---','', '证据提交流程 / Review workflow: [Evidence policy](../EVIDENCE_POLICY.md) · [Report an item](../.github/ISSUE_TEMPLATE/evidence-report.yml)','']
    return '\n'.join(lines)

def publish(scan,now=None):
    now=now or datetime.now(timezone.utc)
    day=now.astimezone(TZ).date().isoformat()
    if scan.get('collected_on')!=day:
        raise ValueError(f'Refusing stale/wrong-day scan: {scan.get("collected_on")} vs {day} Asia/Shanghai')
    if not isinstance(scan.get('leads'),list) or not scan.get('queries_executed'):
        raise ValueError('Invalid scan payload')
    if len(scan.get('failed_queries',[])) >= scan['queries_executed']:
        raise ValueError('Refusing all-feeds-failed scan')
    old=load_json('data/leads.json')
    combined,new_count=merge(old,scan['leads'])
    save_json('data/leads.json',combined)
    state={
        'last_scan_date':day,'last_published_at':now.astimezone(TZ).strftime('%Y-%m-%d %H:%M:%S UTC+8'),
        'new_leads':new_count,'total_leads':len(combined),
        'queries_executed':scan['queries_executed'],'failed_queries':len(scan['failed_queries']),
        'note':'RSS-only multilingual signals, unverified; editorial listings unchanged.',
    }
    save_json('data/monitor_state.json',state)
    (ROOT/'reports/latest.md').write_text(make_report(scan,len(combined)),encoding='utf-8')
    return state

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--input',default='staging/scan.json');args=parser.parse_args()
    scan=__import__('json').loads((ROOT/args.input).read_text(encoding='utf-8'))
    state=publish(scan)
    print(f"Published {state['new_leads']} new unverified leads. No blacklist verdicts changed.")
if __name__=='__main__':main()
