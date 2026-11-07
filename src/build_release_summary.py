import sys
import os
import traceback
import time
import json
import subprocess
import datetime

def get_git_log():
    try:
        repo_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        TOAI_elegant_dir = os.path.join(repo_dir, 'TOAI-elegant-lang')
        if not os.path.exists(os.path.join(TOAI_elegant_dir, '.git')):
            return "Git repository not found in TOAI-elegant-lang."
        
        result = subprocess.run(
            ['git', 'log', '-n', '20', '--oneline'],
            cwd=TOAI_elegant_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout
    except Exception as e:
        return f"Could not retrieve git log: {str(e)}"

def scan_whitepaper():
    try:
        repo_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        whitepaper_path = os.path.join(repo_dir, 'TOAI-elegant-lang', 'WHITEPAPER.md')
        if os.path.exists(whitepaper_path):
            with open(whitepaper_path, 'r', encoding='utf-8') as f:
                content = f.read()
                return content[:1000] + "...\n[Whitepaper truncated]"
        return "Whitepaper not found."
    except Exception as e:
        return f"Could not read whitepaper: {str(e)}"

def main():
    try:
        workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
        os.makedirs(output_dir, exist_ok=True)
        
        git_logs = get_git_log()
        whitepaper_snippet = scan_whitepaper()
        
        summary_data = {
            "timestamp": datetime.datetime.now().isoformat(),
            "git_recent_commits": git_logs,
            "whitepaper_snippet": whitepaper_snippet,
            "status": "success"
        }
        
        output_file = os.path.join(output_dir, 'release_summary.json')
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, ensure_ascii=False, indent=2)
            
        print(f"Release summary successfully generated at {output_file}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
