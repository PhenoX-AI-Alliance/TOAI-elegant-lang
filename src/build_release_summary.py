import sys
import os
import traceback
import subprocess
import json
from datetime import datetime

def get_git_log(repo_path, max_count=20):
    try:
        result = subprocess.run(
            ['git', '-C', repo_path, 'log', f'-n {max_count}', '--pretty=format:%h - %an, %ar : %s'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Git log retrieval failed: {str(e)}"]

def scan_whitepaper(repo_path):
    whitepaper_path = os.path.join(repo_path, 'WHITEPAPER.md')
    if os.path.exists(whitepaper_path):
        try:
            with open(whitepaper_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                return "".join(lines[:30])
        except Exception as e:
            return f"Could not read whitepaper: {str(e)}"
    return "No WHITEPAPER.md found."

def main():
    try:
        workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        repo_path = os.path.join(workspace, 'TOAI-elegant-lang')
        
        if not os.path.exists(os.path.join(repo_path, '.git')):
            print("Git repository not initialized. Initializing for summary generation...")
            subprocess.run(['git', 'init', repo_path], check=True)
            subprocess.run(['git', '-C', repo_path, 'config', 'user.name', 'TOAI Release Agent'], check=True)
            subprocess.run(['git', '-C', repo_path, 'config', 'user.email', 'agent@toai.local'], check=True)
            subprocess.run(['git', '-C', repo_path, 'add', '.'], check=True)
            try:
                subprocess.run(['git', '-C', repo_path, 'commit', '-m', 'Initial commit for release summary'], check=True)
            except Exception:
                pass

        git_logs = get_git_log(repo_path)
        whitepaper_snippet = scan_whitepaper(repo_path)
        
        summary = {
            "timestamp": datetime.now().isoformat(),
            "git_history": git_logs,
            "whitepaper_overview": whitepaper_snippet
        }
        
        output_dir = os.path.join(workspace, 'TOAI_Generated')
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, 'release_summary.json')
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
            
        print(f"Release summary successfully built and saved to {output_file}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
