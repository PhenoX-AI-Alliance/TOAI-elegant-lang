import sys
import os
import traceback
import subprocess
import datetime
import json

def get_git_log(max_count=20):
    try:
        repo_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        target_repo = os.path.join(repo_dir, 'TOAI-elegant-lang')
        if not os.path.exists(os.path.join(target_repo, '.git')):
            target_repo = repo_dir
            
        result = subprocess.run(
            ['git', '-C', target_repo, 'log', f'-n', str(max_count), '--pretty=format:%h - %an, %ar : %s'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except Exception as e:
        return f"Git log retrieval failed: {e}"

def scan_whitepaper():
    try:
        workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        whitepaper_path = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'WHITE_PAPER.md')
        if os.path.exists(whitepaper_path):
            with open(whitepaper_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.splitlines()
                return "\n".join(lines[:30])
        return "Whitepaper not found."
    except Exception as e:
        return f"Whitepaper scan failed: {e}"

def main():
    print("Building release summary...")
    git_history = get_git_log(15)
    whitepaper_summary = scan_whitepaper()
    
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    summary_content = f"""# TOAI Release Summary
Generated at: {timestamp}

## 1. Whitepaper Overview (Excerpt)
{whitepaper_summary}

## 2. Recent Git Commit History
{git_history}
"""
    
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    out_dir = os.path.join(workspace_dir, 'TOAI_Generated')
    os.makedirs(out_dir, exist_ok=True)
    
    out_file = os.path.join(out_dir, 'release_summary.md')
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write(summary_content)
        
    print(f"Release summary successfully built at: {out_file}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
