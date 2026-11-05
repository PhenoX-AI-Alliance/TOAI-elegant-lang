import sys
import os
import traceback
import time
import json
import subprocess
import datetime

def run_git_log():
    repo_path = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    git_dir = os.path.join(repo_path, 'TOAI-elegant-lang')
    if not os.path.exists(os.path.join(git_dir, '.git')):
        git_dir = repo_path
        if not os.path.exists(os.path.join(git_dir, '.git')):
            return "Git repository not found."
            
    try:
        result = subprocess.run(
            ['git', 'log', '-n', '10', '--oneline'],
            cwd=git_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout
    except Exception as e:
        return f"Failed to fetch git log: {str(e)}"

def scan_whitepaper():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    whitepaper_paths = [
        os.path.join(workspace, 'TOAI-elegant-lang', 'WHITESPAPER.md'),
        os.path.join(workspace, 'WHITESPAPER.md'),
        os.path.join(workspace, 'CONSTITUTION.md')
    ]
    
    found_info = []
    for path in whitepaper_paths:
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read(500)
                    found_info.append(f"--- File: {os.path.basename(path)} ---\n{content}\n")
            except Exception as e:
                found_info.append(f"Error reading {path}: {str(e)}")
                
    if not found_info:
        return "No whitepaper or charter files found."
    return "\n".join(found_info)

def generate_summary():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    output_dir = os.path.join(workspace, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    
    git_logs = run_git_log()
    whitepaper_text = scan_whitepaper()
    
    now = datetime.datetime.now().isoformat()
    
    summary_data = {
        "timestamp": now,
        "git_recent_commits": git_logs,
        "whitepaper_excerpt": whitepaper_text,
        "status": "success"
    }
    
    output_file = os.path.join(output_dir, 'release_summary.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, ensure_ascii=False, indent=2)
        
    print(f"Release summary successfully generated at: {output_file}")

if __name__ == '__main__':
    try:
        generate_summary()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
