import sys
import os
import subprocess
import json
import datetime
import traceback

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang')
    
    if not os.path.isdir(repo_dir):
        print(f"Error: Repository directory {repo_dir} does not exist.")
        sys.exit(1)
        
    git_dir = os.path.join(repo_dir, '.git')
    if not os.path.isdir(git_dir):
        print("Initializing git repository for release summary scanning...")
        try:
            subprocess.run(['git', 'init'], cwd=repo_dir, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            subprocess.run(['git', 'config', 'user.name', 'TOAI Builder'], cwd=repo_dir, check=True)
            subprocess.run(['git', 'config', 'user.email', 'builder@toai.local'], cwd=repo_dir, check=True)
            subprocess.run(['git', 'add', '.'], cwd=repo_dir, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            subprocess.run(['git', 'commit', '-m', 'Initial commit for release summary'], cwd=repo_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except Exception as e:
            print(f"Warning during git init/commit: {e}")

    git_logs = "No git history available."
    try:
        res = subprocess.run(['git', 'log', '-n', '10', '--oneline'], cwd=repo_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        git_logs = res.stdout.strip()
    except Exception as e:
        git_logs = f"Could not fetch git logs: {e}"
        
    whitepaper_path = os.path.join(repo_dir, 'WHITEPAPER.md')
    whitepaper_content = "Whitepaper not found."
    if os.path.exists(whitepaper_path):
        try:
            with open(whitepaper_path, 'r', encoding='utf-8') as f:
                whitepaper_content = f.read()[:2000]
        except Exception as e:
            whitepaper_content = f"Error reading whitepaper: {e}"
            
    summary_data = {
        "timestamp": datetime.datetime.now().isoformat(),
        "git_logs": git_logs,
        "whitepaper_excerpt": whitepaper_content,
        "release_status": "stable"
    }
    
    output_file = os.path.join(workspace_dir, 'TOAI_Generated', 'release_summary.json')
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, indent=2, ensure_ascii=False)
        
    print(f"Release summary successfully generated at: {output_file}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
