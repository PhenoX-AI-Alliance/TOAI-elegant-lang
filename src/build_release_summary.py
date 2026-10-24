import sys
import os
import traceback
import subprocess
import json
import datetime

def run_git_command(cmd, cwd):
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Git command failed: {' '.join(cmd)}")
        print(e.stderr)
        return ""
    except Exception as e:
        print(f"Unexpected error running git command: {e}")
        return ""

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_path = os.path.join(workspace_dir, 'TOAI-elegant-lang')
    
    if not os.path.exists(os.path.join(repo_path, '.git')):
        print("Git repository not found at target path. Initializing or searching...")
        sys.exit(1)
        
    print("Scanning git log for release summary...")
    git_log = run_git_command(['git', 'log', '-n', '20', '--pretty=format:%h - %an: %s (%ad)', '--date=short'], repo_path)
    
    whitepaper_path = os.path.join(repo_path, 'WHITEPAPER.md')
    whitepaper_snippet = ""
    if os.path.exists(whitepaper_path):
        try:
            with open(whitepaper_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                whitepaper_snippet = "".join(lines[:30])
        except Exception as e:
            print(f"Could not read WHITEPAPER.md: {e}")
            
    summary_data = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "recent_commits": git_log.splitlines() if git_log else [],
        "whitepaper_overview": whitepaper_snippet
    }
    
    output_path = os.path.join(workspace_dir, 'TOAI_Generated', 'release_summary.json')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, indent=2, ensure_ascii=False)
        
    print(f"Release summary successfully generated at: {output_path}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
