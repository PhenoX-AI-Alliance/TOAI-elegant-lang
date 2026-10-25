import sys
import os
import traceback
import subprocess
import json
from datetime import datetime

def get_git_log(repo_path, max_count=20):
    try:
        cmd = ['git', '-C', repo_path, 'log', f'-n', str(max_count), '--pretty=format:%h - %an, %ar : %s']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Error fetching git log: {str(e)}"]

def scan_whitepaper(repo_path):
    wp_path = os.path.join(repo_path, 'WHITEPAPER.md')
    if os.path.exists(wp_path):
        try:
            with open(wp_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            return ''.join(lines[:30])
        except Exception as e:
            return f"Error reading WHITEPAPER.md: {str(e)}"
    return "WHITEPAPER.md not found."

def main():
    try:
        workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        repo_path = os.path.join(workspace_dir, 'TOAI-elegant-lang')
        
        if not os.path.exists(os.path.join(repo_path, '.git')):
            print("Git repository not initialized. Initializing for summary generation...")
            subprocess.run(['git', 'init', repo_path], check=True)
            subprocess.run(['git', '-C', repo_path, 'config', 'user.name', 'TOAI Builder'], check=True)
            subprocess.run(['git', '-C', repo_path, 'config', 'user.email', 'builder@toai.internal'], check=True)
            
        logs = get_git_log(repo_path)
        whitepaper_snippet = scan_whitepaper(repo_path)
        
        summary = {
            "timestamp": datetime.utcnow().isoformat(),
            "git_logs": logs,
            "whitepaper_snippet": whitepaper_snippet
        }
        
        output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
        os.makedirs(output_dir, exist_ok=True)
        out_path = os.path.join(output_dir, 'release_summary.json')
        
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
            
        print(f"Release summary successfully generated at: {out_path}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
