"""Find today's successful 02:00 artifact-producing GitHub Actions run for publish."""
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from zoneinfo import ZoneInfo


def find_run(runs,day):
    found=[]
    for r in runs:
        if r.get('conclusion')!='success' or r.get('head_branch')!='main': continue
        timestamp=r.get('created_at','')
        if not timestamp:continue
        utc=datetime.fromisoformat(timestamp.replace('Z','+00:00'))
        local=utc.astimezone(ZoneInfo('Asia/Shanghai'))
        if local.date().isoformat()==day and (local.hour>=2):
            found.append((utc,r['id']))
    return max(found)[1] if found else None


def main():
    repo=os.environ['GITHUB_REPOSITORY']
    day=datetime.now(timezone.utc).astimezone(ZoneInfo('Asia/Shanghai')).date().isoformat()
    cmd=['gh','api',f'repos/{repo}/actions/workflows/collect.yml/runs','-f','per_page=100']
    # -f makes gh api POST by default; use explicit GET.
    cmd+=['--method','GET']
    result=subprocess.run(cmd,check=True,text=True,capture_output=True)
    runs=json.loads(result.stdout).get('workflow_runs',[])
    selected=find_run(runs,day)
    if not selected:sys.exit(f'No successful MGGA 02:00 collection for {day} Asia/Shanghai. Publish aborted.')
    print(selected)
if __name__=='__main__':main()
