import sys
import unittest
from pathlib import Path
from datetime import datetime, timezone

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from common import ROOT,load_json,rel_url
from collect import collect,rotating_game_queries,news_url
from publish import merge,make_report,publish
from validate import check
from render import list_section,research_section,row
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
        text=row(sample,'zh')
        self.assertIn('~~',text)
        self.assertIn('测评',text)
    def test_unreviewed_never_leaks_into_public_listing(self):
        games=load_json('data/games.json')
        self.assertEqual(102,len(games))
        public=list_section(games,'zh')
        self.assertNotIn('7 Days to Die',public)
        self.assertNotIn('Assassin',public)
        research=research_section(games,'zh')
        self.assertIn('7 Days to Die',research)
        self.assertIn('Assassin',research)
        self.assertEqual(100,research.count('Not on the public list')+research.count('未进入正式名单'))

    def test_fake_approval_is_rejected(self):
        import copy
        g=copy.deepcopy(load_json('data/games.json')[0])
        g['decision']='listed'
        g['investigation_status']='verified_link'
        g['review_basis']='verified_conduct'
        g['issues']=[{'title_zh':'有出处的事件','title_en':'Sourced claim','evidence_ids':['x']}]
        g['evidence']['player']=[{'id':'x','verification_status':'verified','source_url':'https://example.com/document','file':'research/cases/'+g['game_id']+'.md','checked_at':'2026-10-26'}]
        self.assertTrue(any('editorial approval' in err for err in check([g])))
        self.assertNotIn(g['title_en'],list_section([g],'en'))

    def test_verified_approval_qualifies(self):
        import copy
        g=copy.deepcopy(load_json('data/games.json')[0])
        g['decision']='listed'
        g['investigation_status']='verified_link'
        g['review_basis']='verified_conduct'
        g['editorial_approval']={'status':'approved','reviewed_by':'maintainer','reviewed_at':'2026-10-26'}
        g['issues']=[{'title_zh':'具体已核实事项','title_en':'Specific documented finding','evidence_ids':['x']}]
        g['evidence']['player']=[{'id':'x','verification_status':'verified','source_url':'https://example.com/original','file':'research/cases/'+g['game_id']+'.md','checked_at':'2026-10-26'}]
        self.assertEqual([],check([g]))
        self.assertIn(g['title_en'],list_section([g],'en'))

    def test_controversy_requires_multiple_sources_and_labels(self):
        import copy
        g=copy.deepcopy(load_json('data/games.json')[0])
        g['decision']='listed'
        g['investigation_status']='disputed'
        g['review_basis']='documented_player_controversy'
        g['editorial_approval']={'status':'approved','reviewed_by':'maintainer','reviewed_at':'2026-10-26'}
        g['issues']=[{'title_zh':'公开争议','title_en':'Documented controversy','claim_status':'disputed','evidence_ids':['a','b','c']}]
        g['evidence']['player']=[{'id':v,'verification_status':'verified','source_url':url,'file':'research/cases/'+g['game_id']+'.md','checked_at':'2026-10-26'} for v,url in [('a','https://one.example/1'),('b','https://two.example/2'),('c','https://one.example/3')]]
        self.assertEqual([],check([g]))
        g['evidence']['player']=g['evidence']['player'][:2]
        self.assertTrue(check([g]))

    def test_full_render_never_leaks_unreviewed_names(self):
        import json
        from render import main as render_main
        render_main()
        public_cn=(ROOT/'README.md').read_text(encoding='utf-8')
        public_en=(ROOT/'README.en.md').read_text(encoding='utf-8')
        self.assertIn('独立调查登记册',public_cn)
        self.assertNotIn('7 Days to Die',public_cn)
        self.assertNotIn('7 Days to Die',public_en)
        self.assertNotIn('首批100款热门游戏',public_cn)
        self.assertIn('7 Days to Die',(ROOT/'research'/'README.md').read_text(encoding='utf-8'))
        self.assertIn('7 Days to Die',(ROOT/'research'/'README.en.md').read_text(encoding='utf-8'))
        self.assertEqual(2,len(json.loads((ROOT/'docs'/'search-index.json').read_text(encoding='utf-8'))))
        self.assertTrue(public_cn.strip().endswith('</p>'))
        self.assertIn('Powered by Codex',public_en)
        self.assertIn('Concord',public_en)
        self.assertIn('Dying Light 2 Stay Human',public_cn)

    def test_personal_aesthetic_cases_listed_only_when_approved(self):
        import copy
        games=load_json('data/games.json')
        approved=[g for g in games if g['decision']=='listed']
        self.assertEqual({'Concord','Dying Light 2 Stay Human'},{g['title_en'] for g in approved})
        self.assertTrue(all(g['review_basis']=='personal_aesthetic' for g in approved))
        text=list_section(games,'zh')
        self.assertIn('Concord',text)
        self.assertNotIn('7 Days to Die',text)
        altered=copy.deepcopy(approved[0])
        altered['issues'][0]['claim_status']='verified'
        self.assertTrue(check([altered]))
        altered=copy.deepcopy(approved[0])
        altered['evidence']['promotional']=[]
        self.assertTrue(check([altered]))

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
