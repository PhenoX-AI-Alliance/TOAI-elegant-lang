import sys
import os
import subprocess
import json
import datetime

def get_git_log(max_count=10):
    repo_path = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    git_dir = os.path.join(repo_path, 'TOAI-elegant-lang')
    if not os.path.exists(os.path.join(git_dir, '.git')):
        git_dir = repo_path
    
    try:
        cmd = ['git', '-C', git_dir, 'log', f'-n', str(max_count), '--pretty=format:%h - %an: %s (%ad)']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Git log retrieval failed: {str(e)}"]

def scan_whitepaper():
    repo_path = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    whitepaper_candidates = [
        os.path.join(repo_path, 'TOAI-elegant-lang', 'WHITEPAPER.md'),
        os.path.join(repo_path, 'WHITEPAPER.md')
    ]
    for path in whitepaper_candidates:
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    return "".join(lines[:20])
            except Exception:
                pass
    return "Whitepaper not found."

def build_summary():
    logs = get_git_log(15)
    wp_excerpt = scan_whitepaper()
    now = datetime.datetime.now().isoformat()
    
    summary = {
        "timestamp": now,
        "version_overview": wp_excerpt.strip(),
        "recent_commits": logs
    }
    
    repo_path = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    out_path = os.path.join(repo_path, 'TOAI_Generated', 'release_summary.json')
    
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    print(f"Release summary successfully generated at: {out_path}")

if __name__ == '__main__':
    build_summary()
