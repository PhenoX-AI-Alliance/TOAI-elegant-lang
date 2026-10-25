import sys
import os
import subprocess
import json
import glob
from datetime import datetime

def get_git_log():
    try:
        res = subprocess.run(
            ['git', 'log', '-n', '10', '--pretty=format:%h - %an: %s (%ad)'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return res.stdout.splitlines()
    except Exception as e:
        return [f"Git log unavailable: {str(e)}"]

def scan_whitepapers():
    ws_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    pattern = os.path.join(ws_dir, '**', '*.md')
    files = glob.glob(pattern, recursive=True)
    summaries = []
    for f in sorted(files)[:5]:
        try:
            with open(f, 'r', encoding='utf-8') as file:
                content = file.read(200)
                summaries.append({'path': f, 'snippet': content.strip().replace('\n', ' ')})
        except Exception:
            pass
    return summaries

def main():
    print("Building release summary...")
    logs = get_git_log()
    papers = scan_whitepapers()
    
    report = {
        "timestamp": datetime.now().isoformat(),
        "recent_commits": logs,
        "whitepaper_snippets": papers
    }
    
    out_path = os.path.join(os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/'), 'TOAI_Generated', 'release_summary.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully generated release summary at: {out_path}")

if __name__ == '__main__':
    main()
