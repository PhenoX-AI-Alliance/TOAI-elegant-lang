import sys
import os
import subprocess
import json
import datetime

def get_git_log():
    try:
        res = subprocess.run(
            ['git', 'log', '-n', '10', '--oneline'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return res.stdout.strip().splitlines()
    except Exception as e:
        return [f"Git log unavailable: {e}"]

def scan_whitepaper():
    base_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    target_files = ['WHITE_PAPER.md', 'README.md', 'CONSTITUTION.md']
    summary = {}
    for fname in target_files:
        fpath = os.path.join(base_dir, fname)
        if os.path.exists(fpath):
            try:
                with open(fpath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    summary[fname] = content[:300] + "..." if len(content) > 300 else content
            except Exception as e:
                summary[fname] = f"Error reading: {e}"
        else:
            summary[fname] = "Not found"
    return summary

def main():
    print("=== TOAI Release Summary Builder ===")
    git_logs = get_git_log()
    whitepaper_data = scan_whitepaper()
    
    release_info = {
        "timestamp": datetime.datetime.now().isoformat(),
        "git_recent_commits": git_logs,
        "whitepaper_summary": whitepaper_data
    }
    
    base_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    out_dir = os.path.join(base_dir, 'TOAI_Generated')
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, 'release_summary.json')
    
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(release_info, f, ensure_ascii=False, indent=2)
        
    print(f"Successfully generated release summary at: {out_path}")

if __name__ == '__main__':
    main()
