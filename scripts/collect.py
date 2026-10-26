"""02:00 Asia/Shanghai: public news-RSS lead discovery. No accusations or decisions.

Only an ephemeral Actions artifact is produced. No repository write at 02:00.
Feeds may be unavailable by geography, rate-limits or upstream changes.
"""
from __future__ import annotations
import argparse
import email.utils
import hashlib
import html
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from xml.etree import ElementTree as ET
from zoneinfo import ZoneInfo
from common import ROOT, load_json

TZ=ZoneInfo('Asia/Shanghai')

def clean_html(value):
    return re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]*>', ' ',value or ''))).strip()[:600]

def news_url(config):
    params={"q":config['query']+' when:2d',"hl":config['hl'],"gl":config['gl'],"ceid":config['ceid']}
    return 'https://news.google.com/rss/search?'+urlencode(params)

def read_feed(xml_bytes,config,seen_at):
    root=ET.fromstring(xml_bytes)
    output=[]
    for item in root.findall('./channel/item')[:35]:
        title=clean_html(item.findtext('title'))
        url=(item.findtext('link') or '').strip()
        if not title or not url.startswith('https://'): continue
        # Google News can expose an aggregation/redirect URL. Don't represent it as an original primary source.
        pub=item.findtext('pubDate') or ''
        try:
            published=email.utils.parsedate_to_datetime(pub).astimezone(timezone.utc).isoformat()
        except (TypeError, ValueError): published=None
        source=item.find('source')
        source_name=clean_html(source.text if source is not None else '') or 'Unknown'
        source_site=source.attrib.get('url','') if source is not None else ''
        key=re.sub(r'\W+',' ',title.casefold()).strip()+'|'+source_name.casefold()
        lead_id=hashlib.sha256(key.encode('utf-8')).hexdigest()[:20]
        output.append({
            'id':lead_id,'headline':title,'aggregator_url':url,
            'source_name':source_name,'source_site':source_site,
            'summary':clean_html(item.findtext('description')),
            'published_at':published,'first_seen_at':seen_at,
            'languages':[config['language']],'matched_queries':[config['id']],
            'facets':[config.get('focus','issue')],
            'verification_status':'unverified',
        })
    return output

def collect(configs,fetch=None,now=None):
    now=now or datetime.now(timezone.utc)
    seen_at=now.isoformat(timespec='seconds')
    collector=fetch or _fetch
    by_id={}; failed=[]
    for config in configs:
        try:
            for item in read_feed(collector(news_url(config)),config,seen_at):
                old=by_id.get(item['id'])
                if old:
                    for key in ('matched_queries','languages','facets'):
                        old[key]=sorted(set(old[key])|set(item[key]))
                else: by_id[item['id']]=item
        except Exception as exc:
            # Avoid leaking arbitrary feed bodies; status message is diagnostic only.
            failed.append({'query':config['id'],'error':f'{type(exc).__name__}: {str(exc)[:150]}'})
    leads=list(by_id.values())
    leads.sort(key=lambda x:(x.get('published_at') or '',x['headline']),reverse=True)
    return {
        'schema_version':1,'collected_on':now.astimezone(TZ).date().isoformat(),
        'collected_at':seen_at,'queries_executed':len(configs),
        'failed_queries':failed,'leads':leads[:350],
        'scope_notice':'Unverified multilingual RSS discovery leads, not a complete global games catalog.',
    }

def _fetch(url):
    req=Request(url,headers={'User-Agent':'MGGA-OpenSource-LeadCollector/1.0 (public RSS, no scraping private data)','Accept':'application/rss+xml,application/xml'})
    with urlopen(req,timeout=16) as r:
        return r.read(1_500_000)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',default='out/scan.json');args=ap.parse_args()
    configs=load_json('data/monitor_queries.json')
    scan=collect(configs)
    p=ROOT/args.output;p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(scan,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(f"MGGA discovery {scan['collected_on']}: {len(scan['leads'])} leads; {len(scan['failed_queries'])}/{len(configs)} feeds failed.")
    if len(scan['failed_queries'])==len(configs):
        sys.exit('All RSS feeds failed. Do not publish a success-looking empty scan.')
if __name__=='__main__':main()
