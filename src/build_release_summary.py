import sys
import os
import traceback
import subprocess
import json

def get_git_log():
    try:
        repo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        if not os.path.exists(os.path.join(repo_path, '.git')):
            return "Git repository not initialized."
        result = subprocess.run(
            ['git', 'log', '-n', '10', '--oneline'],
            cwd=repo_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout
    except Exception as e:
        return f"Could not retrieve git log: {e}"

def scan_whitepaper():
    try:
        repo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        wp_path = os.path.join(repo_path, 'WHITEPAPER.md')
        if os.path.exists(wp_path):
            with open(wp_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            return "".join(lines[:30])
        return "Whitepaper not found."
    except Exception as e:
        return f"Could not read whitepaper: {e}"

def main():
    print("Generating release summary...")
    git_logs = get_git_log()
    whitepaper_snippet = scan_whitepaper()
    
    summary = {
        "version": "1.0.0",
        "git_recent_commits": git_logs.splitlines(),
        "whitepaper_overview": whitepaper_snippet
    }
    
    output_dir = os.path.join(os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/'), 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = os.path.join(output_dir, 'release_summary.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    print(f"Successfully generated release summary at: {output_file}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
