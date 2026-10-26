"""Validate curated records before publication. No allegations from unreviewed leads."""
import sys
import re
from datetime import date
from urllib.parse import urlparse
from common import ROOT, CATEGORIES, evidence_path, load_json

INVESTIGATION = {'unreviewed','investigating','verified_link','disputed','no_verified_link'}
DECISIONS = {'pending','listed','remediated','not_listed'}

def valid_url(v):
    try:
        p=urlparse(v)
        return p.scheme == 'https' and bool(p.hostname)
    except (TypeError, ValueError):
        return False

def check(games, check_files=True):
    errs=[]
    seen_ids=set()
    for i,g in enumerate(games):
        key=f"row {i+1} ({g.get('game_id', '?')})"
        for field in ('game_id','title_en','title_zh','release_date','platforms','official_url','investigation_status','decision','issues','evidence','remediation'):
            if field not in g: errs.append(f'{key}: missing {field}')
        if any(k not in g for k in ('game_id','title_en','title_zh','release_date','platforms','official_url','investigation_status','decision','issues','evidence','remediation')): continue
        gid=g['game_id']
        if gid in seen_ids: errs.append(f'{key}: duplicate game_id')
        seen_ids.add(gid)
        if not isinstance(gid,str) or not gid or any(ch not in 'abcdefghijklmnopqrstuvwxyz0123456789-' for ch in gid):
            errs.append(f'{key}: game_id must be lower-case kebab-case ascii')
        try:
            d=g['release_date']
            if not isinstance(d,str) or not re.fullmatch(r'\d{4}(?:-\d{2}(?:-\d{2})?)?',d):
                raise ValueError('Bad precision')
            date.fromisoformat(d if len(d)==10 else (d+'-01' if len(d)==7 else d+'-01-01'))
        except (TypeError, ValueError): errs.append(f'{key}: invalid date')
        if not isinstance(g['platforms'],list) or not g['platforms']: errs.append(f'{key}: platforms needed')
        if not valid_url(g['official_url']): errs.append(f'{key}: official_url must be https URL')
        if g['investigation_status'] not in INVESTIGATION: errs.append(f'{key}: invalid investigation_status')
        if g['decision'] not in DECISIONS: errs.append(f'{key}: invalid decision')
        ev=g['evidence']
        if not isinstance(ev,dict) or any(k not in ev for k in ('reviews','promotional','player')):
            errs.append(f'{key}: missing evidence categories'); continue
        verified_ids=set()
        for kind in ('reviews','promotional','player'):
            if not isinstance(ev[kind],list): errs.append(f'{key}: {kind} must be list'); continue
            for e in ev[kind]:
                if e.get('verification_status') == 'verified' and valid_url(e.get('source_url')) and e.get('id') and e.get('file') and e.get('checked_at'):
                    verified_ids.add(e['id'])
                    if check_files and not (ROOT / e['file']).is_file(): errs.append(f"{key}: missing evidence file {e['file']}")
                elif e.get('verification_status') not in {'unverified','disputed','verified'}:
                    errs.append(f'{key}: invalid evidence verification status')
                elif e.get('verification_status') == 'verified':
                    errs.append(f'{key}: verified evidence missing provenance')
        if g['decision'] in {'listed','remediated'}:
            # Fail closed: publication requires a documented, dated human decision.
            basis=g.get('review_basis')
            approval=g.get('editorial_approval')
            if basis not in {'verified_conduct','documented_player_controversy'}:
                errs.append(f'{key}: listed/remediated requires a recognized review_basis')
            expected='disputed' if basis=='documented_player_controversy' else 'verified_link'
            if g['investigation_status'] != expected:
                errs.append(f'{key}: investigation_status must be {expected} for chosen review basis')
            if not isinstance(approval,dict) or approval.get('status')!='approved' or not approval.get('reviewed_by') or not approval.get('reviewed_at'):
                errs.append(f'{key}: listed/remediated requires dated human editorial approval')
            else:
                try: date.fromisoformat(approval['reviewed_at'])
                except (TypeError,ValueError): errs.append(f'{key}: human approval date must be YYYY-MM-DD')
            if not g['issues']: errs.append(f'{key}: listed/remediated requires documented specific issues')
            for issue in g['issues']:
                ids=issue.get('evidence_ids',[])
                if not ids or not set(ids).issubset(verified_ids):
                    errs.append(f'{key}: issue needs source-backed verified evidence IDs')
                if not issue.get('title_zh') or not issue.get('title_en'):
                    errs.append(f'{key}: issue needs bilingual specific titles')
                if basis=='documented_player_controversy' and issue.get('claim_status')!='disputed':
                    errs.append(f'{key}: community controversy must label the underlying claim disputed')
            if basis=='documented_player_controversy':
                # Three independently located records spanning >=2 sites;
                # verifies the existence of a public controversy, not an allegation's truth.
                player_urls={e.get('source_url') for e in ev.get('player',[])
                             if isinstance(e,dict) and e.get('id') in verified_ids and valid_url(e.get('source_url'))}
                hosts={urlparse(u).hostname.lower() for u in player_urls}
                if len(player_urls)<3 or len(hosts)<2:
                    errs.append(f'{key}: public controversy requires >=3 verified distinct player-discussion sources on >=2 hostnames')
            if check_files:
                for kind in CATEGORIES:
                    p=ROOT/evidence_path(kind,gid)
                    if not p.is_file(): errs.append(f'{key}: missing evidence-category README: {p}')
        remediation=g['remediation']
        if g['decision'] == 'remediated':
            if remediation.get('status') != 'completed' or not remediation.get('date') or not remediation.get('sources'):
                errs.append(f'{key}: remediated requires dated, source-backed remediation')
            elif any(not valid_url(url) for url in remediation['sources']):
                errs.append(f'{key}: invalid remediation source URL')
    return errs

if __name__ == '__main__':
    problems=check(load_json('data/games.json'))
    if problems:
        print('\n'.join(problems),file=sys.stderr); sys.exit(1)
    print('MGGA curated data validation passed.')
