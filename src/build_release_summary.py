import sys
import os
import subprocess
import json
import datetime

def get_git_log(max_count=20):
    try:
        repo_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        git_path = os.path.join(repo_dir, 'TOAI-elegant-lang')
        if not os.path.exists(os.path.join(git_path, '.git')):
            git_path = repo_dir
            
        result = subprocess.run(
            ['git', 'log', f'-n', str(max_count), '--pretty=format:%h - %an, %ar : %s'],
            cwd=git_path,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Git log retrieval failed: {str(e)}"]

def scan_whitepaper():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    whitepaper_candidates = [
        os.path.join(workspace_dir, 'WHITEPAPER.md'),
        os.path.join(workspace_dir, 'TOAI-elegant-lang', 'WHITEPAPER.md')
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
    print("=== TOAI Release Summary Builder ===")
    logs = get_git_log()
    whitepaper_snippet = scan_whitepaper()
    
    summary = {
        "timestamp": datetime.datetime.now().isoformat(),
        "git_commits": logs,
        "whitepaper_overview": whitepaper_snippet
    }
    
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    out_path = os.path.join(workspace_dir, 'TOAI_Generated', 'release_summary.json')
    
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
        
    print(f"Release summary successfully generated at: {out_path}")

if __name__ == '__main__':
    main()
