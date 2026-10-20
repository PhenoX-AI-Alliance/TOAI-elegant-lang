import sys
import os
import traceback
import subprocess
import json
from datetime import datetime

def get_git_log(max_count=20):
    try:
        cmd = ['git', 'log', f'-n', str(max_count), '--pretty=format:%h - %an, %ar : %s']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True, encoding='utf-8')
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Git log retrieval failed: {str(e)}"]

def scan_whitepaper():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    potential_paths = [
        os.path.join(workspace_dir, 'WHITE_PAPER.md'),
        os.path.join(workspace_dir, 'docs', 'WHITE_PAPER.md'),
        os.path.join(workspace_dir, 'TOAI-elegant-lang', 'WHITE_PAPER.md')
    ]
    for path in potential_paths:
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    return f.read()[:2000]
            except Exception:
                pass
    return "Whitepaper not found in standard locations."

def generate_release_summary():
    logs = get_git_log()
    whitepaper_snippet = scan_whitepaper()
    
    summary = {
        "timestamp": datetime.now().isoformat(),
        "recent_commits": logs,
        "whitepaper_excerpt": whitepaper_snippet
    }
    
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    
    out_file = os.path.join(output_dir, 'release_summary.json')
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
        
    print(f"Release summary successfully generated at: {out_file}")

if __name__ == '__main__':
    try:
        generate_release_summary()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
