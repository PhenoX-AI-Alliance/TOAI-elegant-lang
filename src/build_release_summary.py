import sys
import os
import traceback
import subprocess
import json
import datetime

def run_git_log():
    repo_path = os.path.join(os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/'), 'TOAI-elegant-lang')
    if not os.path.exists(os.path.join(repo_path, '.git')):
        return "Git repository not initialized or path invalid."
    try:
        result = subprocess.run(
            ['git', '-C', repo_path, 'log', '-n', '10', '--oneline'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Git command failed: {e}"

def scan_whitepaper():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    wp_path = os.path.join(workspace, 'TOAI-elegant-lang', 'WHITEPAPER.md')
    if os.path.exists(wp_path):
        try:
            with open(wp_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            return "".join(lines[:20])
        except Exception as e:
            return f"Failed to read whitepaper: {e}"
    return "Whitepaper not found."

def main():
    try:
        workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        output_dir = os.path.join(workspace, 'TOAI_Generated')
        os.makedirs(output_dir, exist_ok=True)
        
        git_logs = run_git_log()
        whitepaper_snippet = scan_whitepaper()
        
        summary = {
            "timestamp": datetime.datetime.now().isoformat(),
            "git_recent_commits": git_logs,
            "whitepaper_overview": whitepaper_snippet
        }
        
        output_file = os.path.join(output_dir, 'release_summary.json')
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
            
        print(f"Successfully generated release summary at: {output_file}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
