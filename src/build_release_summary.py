import sys
import os
import subprocess
import json
import datetime

def get_git_log(max_count=10):
    try:
        result = subprocess.run(
            ['git', 'log', f'-n', str(max_count), '--pretty=format:%h - %an, %ar : %s'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Git log retrieval failed: {str(e)}"]

def scan_whitepaper():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    candidates = ['WHITE_PAPER.md', 'README.md', 'CONSTITUTION.md']
    summary = {}
    for cand in candidates:
        path = os.path.join(workspace, cand)
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    summary[cand] = content[:300] + "..." if len(content) > 300 else content
            except Exception as e:
                summary[cand] = f"Error reading file: {str(e)}"
    return summary

def generate_release_summary():
    logs = get_git_log(15)
    whitepaper_info = scan_whitepaper()
    
    release_data = {
        "timestamp": datetime.datetime.now().isoformat(),
        "git_history": logs,
        "whitepaper_snippets": whitepaper_info,
        "version": "1.0.0-gaia"
    }
    
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    out_path = os.path.join(workspace, 'TOAI_Generated', 'release_summary.json')
    
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(release_data, f, ensure_ascii=False, indent=2)
    
    print(f"Release summary successfully generated at: {out_path}")

if __name__ == '__main__':
    generate_release_summary()
