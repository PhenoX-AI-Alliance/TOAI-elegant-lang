import sys
import os
import traceback
import time
import json
import subprocess
import datetime

def get_git_log(repo_path, max_count=20):
    try:
        cmd = ['git', '-C', repo_path, 'log', f'-n', str(max_count), '--pretty=format:%h - %an: %s (%ad)', '--date=short']
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        return result.stdout.strip().split('\n')
    except Exception as e:
        return [f"Git log retrieval failed: {str(e)}"]

def scan_whitepaper(workspace_path):
    whitepaper_path = os.path.join(workspace_path, 'WHITEPAPER.md')
    if os.path.exists(whitepaper_path):
        try:
            with open(whitepaper_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            return "".join(lines[:50])
        except Exception as e:
            return f"Failed to readWHITEPAPER.md: {str(e)}"
    return "WHITEPAPER.md not found."

def main():
    try:
        workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        repo_path = os.path.join(workspace_dir, 'TOAI-elegant-lang')
        
        if not os.path.exists(os.path.join(repo_path, '.git')):
            print(f"Initializing git repository at {repo_path}")
            os.makedirs(repo_path, exist_ok=True)
            subprocess.run(['git', 'init', repo_path], check=True)
            
        git_logs = get_git_log(repo_path)
        whitepaper_snippet = scan_whitepaper(workspace_dir)
        
        summary_data = {
            "timestamp": datetime.datetime.now().isoformat(),
            "git_history": git_logs,
            "whitepaper_overview": whitepaper_snippet
        }
        
        output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
        os.makedirs(output_dir, exist_ok=True)
        
        output_file = os.path.join(output_dir, 'release_summary.json')
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, ensure_ascii=False, indent=4)
            
        print(f"Successfully generated release summary at {output_file}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
