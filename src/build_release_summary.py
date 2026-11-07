import sys
import os
import traceback
import time
import json
import subprocess
from datetime import datetime

def get_git_log(repo_path, max_count=20):
    try:
        result = subprocess.run(
            ['git', '-C', repo_path, 'log', f'-n', str(max_count), '--pretty=format:%h - %an, %ar: %s'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Git log retrieval failed: {str(e)}"]

def scan_whitepaper(repo_path):
    whitepaper_paths = [
        os.path.join(repo_path, 'WHITEPAPER.md'),
        os.path.join(repo_path, 'docs', 'WHITEPAPER.md'),
        os.path.join(repo_path, 'CONSTITUTION.md')
    ]
    found_info = {}
    for path in whitepaper_paths:
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    found_info[os.path.basename(path)] = f.read()[:500] + "..."
            except Exception as e:
                found_info[os.path.basename(path)] = f"Error reading: {str(e)}"
    return found_info

def main():
    try:
        workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        repo_path = os.path.join(workspace_dir, 'TOAI-elegant-lang')
        
        if not os.path.exists(repo_path):
            os.makedirs(repo_path, exist_ok=True)
            try:
                subprocess.run(['git', 'init', repo_path], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            except Exception:
                pass

        git_logs = get_git_log(repo_path)
        whitepaper_data = scan_whitepaper(repo_path)
        
        summary = {
            "timestamp": datetime.now().isoformat(),
            "version_summary": "TOAI Elegant Lang Release Summary Generator",
            "git_recent_commits": git_logs,
            "whitepaper_snippets": whitepaper_data
        }
        
        output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, 'release_summary.json')
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=4)
            
        print(f"Successfully generated release summary at: {output_file}")
        
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
