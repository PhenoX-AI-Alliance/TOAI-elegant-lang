import sys
import os
import subprocess
import json
import datetime

def run_git_command(cmd, cwd):
    try:
        res = subprocess.run(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        return res.stdout.strip()
    except Exception as e:
        print(f"Git command failed: {e}")
        return ""

def main():
    repo_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    print(f"Scanning repository at: {repo_dir}")
    
    git_status = run_git_command(['git', 'status', '--porcelain'], repo_dir)
    git_log = run_git_command(['git', 'log', '-n', '10', '--oneline'], repo_dir)
    
    whitepaper_path = os.path.join(repo_dir, 'TOAI-elegant-lang', 'WHITEPAPER.md')
    whitepaper_content = ""
    if os.path.exists(whitepaper_path):
        with open(whitepaper_path, 'r', encoding='utf-8') as f:
            whitepaper_content = f.read()
    else:
        whitepaper_content = "Whitepaper not found."
        
    summary = {
        "timestamp": datetime.datetime.now().isoformat(),
        "git_status": git_status.splitlines() if git_status else [],
        "recent_commits": git_log.splitlines() if git_log else [],
        "whitepaper_snippet": whitepaper_content[:500] + ("..." if len(whitepaper_content) > 500 else "")
    }
    
    output_dir = os.path.join(repo_dir, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, 'release_summary.json')
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
        
    print(f"Release summary successfully built at: {output_file}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"Error in build_release_summary: {e}")
        sys.exit(1)
