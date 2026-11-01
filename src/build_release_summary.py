import sys
import os
import traceback
import time
import json
import subprocess
import datetime

def get_git_logs():
    repo_path = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    git_dir = os.path.join(repo_path, 'TOAI-elegant-lang')
    if not os.path.exists(os.path.join(git_dir, '.git')):
        git_dir = repo_path
    
    try:
        result = subprocess.run(
            ['git', '-C', git_dir, 'log', '-n', '20', '--pretty=format:%h - %an, %ar : %s'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except Exception as e:
        return f"Could not retrieve git logs: {e}"

def scan_whitepaper():
    repo_path = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    potential_paths = [
        os.path.join(repo_path, 'TOAI-elegant-lang', 'WHITE_PAPER.md'),
        os.path.join(repo_path, 'WHITE_PAPER.md'),
        os.path.join(repo_path, 'TOAI_Generated', 'WHITE_PAPER.md')
    ]
    
    for path in potential_paths:
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    return content[:1500] # Return summary snippet
            except Exception as e:
                pass
    return "No whitepaper found or failed to read."

def main():
    try:
        workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
        os.makedirs(output_dir, exist_ok=True)
        
        git_logs = get_git_logs()
        whitepaper_snippet = scan_whitepaper()
        
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        summary_data = {
            "timestamp": timestamp,
            "git_logs": git_logs,
            "whitepaper_summary": whitepaper_snippet,
            "status": "success",
            "message": "Release summary successfully generated with altruistic clarity."
        }
        
        output_file = os.path.join(output_dir, 'release_summary.json')
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, ensure_ascii=False, indent=2)
            
        print(f"Successfully generated release summary at {output_file}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
