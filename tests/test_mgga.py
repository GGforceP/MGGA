import sys
import unittest
from pathlib import Path
from datetime import datetime, timezone

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from common import ROOT,load_json,rel_url
from collect import collect,rotating_game_queries,news_url
from publish import merge,make_report,publish
from validate import check
from render import list_section
from get_scan_run import find_run

RSS=b'''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"><channel><item><title>Sample company issued a statement</title>
<link>https://news.google.com/rss/articles/one</link><pubDate>Mon, 26 Oct 2026 01:00:00 GMT</pubDate>
<source url="https://example.org">News source</source><description>Context here.</description></item></channel></rss>'''

class MGGATest(unittest.TestCase):
    def test_curated_data(self): self.assertEqual([],check(load_json('data/games.json')))
    def test_game_rotation_targets_20(self):
        games=load_json('data/games.json')
        q=rotating_game_queries(games,datetime(2026,10,26,tzinfo=timezone.utc))
        self.assertEqual(20,len(q))
        self.assertEqual(20,len({x['id'] for x in q}))
        self.assertTrue(all(x.get('lookback_days')==12 for x in q))
        self.assertTrue(all(x['focus']=='game_issue' for x in q))
    def test_collect_dedup_does_not_verify(self):
        cfg=[{'id':'a','language':'en','hl':'en-US','gl':'US','ceid':'US:en','query':'x'},
             {'id':'b','language':'zh','hl':'zh-CN','gl':'CN','ceid':'CN:zh-Hans','query':'x'}]
        result=collect(cfg,fetch=lambda _:RSS,now=datetime(2026,10,26,18,0,tzinfo=timezone.utc))
        self.assertEqual(1,len(result['leads']))
        self.assertEqual(['a','b'],result['leads'][0]['matched_queries'])
        self.assertEqual('unverified',result['leads'][0]['verification_status'])
        self.assertEqual('2026-10-27',result['collected_on'])
    def test_guard_listing_without_evidence(self):
        sample=load_json('data/games.json')[0].copy();sample['decision']='listed'
        self.assertTrue(check([sample]))
    def test_history_has_strike(self):
        sample=load_json('data/games.json')[0].copy();sample['decision']='remediated';sample['issues']=[{'title_zh':'具体事项','title_en':'Specific issue'}]
        text=list_section([sample],'zh')
        self.assertIn('~~',text)
        self.assertIn('测评',text)
    def test_no_listed_examples(self):
        text=list_section(load_json('data/games.json'),'zh')
        self.assertIn('暂无',text)
    def test_merge_preserves_first_seen(self):
        item={'id':'1','languages':['en'],'matched_queries':['q1'],'first_seen_at':'a','last_seen_at':'a'}
        upd={**item,'languages':['zh'],'matched_queries':['q2'],'first_seen_at':'b'}
        rows,new=merge([item],[upd]);self.assertEqual(0,new)
        self.assertEqual('a',rows[0]['first_seen_at']);self.assertEqual('b',rows[0]['last_seen_at'])
        self.assertEqual(['q1','q2'],rows[0]['matched_queries'])
    def test_choose_today_scan(self):
        runs=[{'conclusion':'success','head_branch':'main','created_at':'2026-10-26T18:03:00Z','id':42},
              {'conclusion':'success','head_branch':'main','created_at':'2026-10-25T18:03:00Z','id':41}]
        self.assertEqual(42,find_run(runs,'2026-10-27'))
    def test_path_encoding(self): self.assertIn('%20',rel_url('附加材料 (Supplementary Materials)/证据 (Evidence)/'))
    def test_report_is_unverified(self):
        report=make_report({'collected_on':'2026-10-27','leads':[],'failed_queries':[],'queries_executed':2},0)
        self.assertIn('未经核实',report)

if __name__=='__main__':unittest.main()
