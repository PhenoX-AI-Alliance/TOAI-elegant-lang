# -*- coding: utf-8 -*-
import sys
import os
import traceback
import subprocess
import json
from datetime import datetime

def get_git_log():
    try:
        result = subprocess.run(
            ['git', 'log', '-n', '10', '--pretty=format:%h - %an: %s (%ad)'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Git log retrieval failed: {str(e)}"]

def scan_whitepaper(workspace_dir):
    whitepaper_candidates = [
        os.path.join(workspace_dir, 'WHITE_PAPER.md'),
        os.path.join(workspace_dir, 'docs', 'WHITE_PAPER.md'),
        os.path.join(workspace_dir, 'TOAI_Generated', 'WHITE_PAPER.md')
    ]
    for path in whitepaper_candidates:
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    return f.read()[:1000]
            except Exception:
                pass
    return "Whitepaper not found or unreadable."

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    release_dir = os.path.join(workspace_dir, 'TOAI_Generated', 'releases')
    os.makedirs(release_dir, exist_ok=True)
    
    logs = get_git_log()
    whitepaper_snippet = scan_whitepaper(workspace_dir)
    
    summary = {
        "timestamp": datetime.now().isoformat(),
        "git_logs": logs,
        "whitepaper_summary": whitepaper_snippet,
        "status": "success",
        "message": "Release summary successfully compiled with altruistic warmth."
    }
    
    output_file = os.path.join(release_dir, f"release_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
        
    print(f"Release summary generated at: {output_file}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
