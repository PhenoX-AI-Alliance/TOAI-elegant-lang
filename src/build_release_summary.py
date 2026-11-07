import sys
import os
import traceback
import subprocess
import json
from datetime import datetime

def get_git_log(max_count=10):
    try:
        repo_path = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        TOAI_elegant_path = os.path.join(repo_path, 'TOAI-elegant-lang')
        if not os.path.exists(os.path.join(TOAI_elegant_path, '.git')):
            # Fallback to workspace root if TOAI-elegant-lang is not its own repo
            TOAI_elegant_path = repo_path
            
        cmd = ['git', '-C', TOAI_elegant_path, 'log', f'-n', str(max_count), '--pretty=format:%h - %an, %ar : %s']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Error fetching git log: {str(e)}"]

def scan_whitepaper():
    try:
        repo_path = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        whitepaper_candidates = [
            os.path.join(repo_path, 'WHITEPAPER.md'),
            os.path.join(repo_path, 'TOAI-elegant-lang', 'WHITEPAPER.md'),
            os.path.join(repo_path, 'docs', 'WHITEPAPER.md')
        ]
        for path in whitepaper_candidates:
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                return ''.join(lines[:30]) # Return first 30 lines as summary
        return "Whitepaper not found in standard locations."
    except Exception as e:
        return f"Error scanning whitepaper: {str(e)}"

def main():
    try:
        workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
        os.makedirs(output_dir, exist_ok=True)
        
        git_logs = get_git_log(15)
        whitepaper_summary = scan_whitepaper()
        
        release_data = {
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0-gaia",
            "git_recent_commits": git_logs,
            "whitepaper_excerpt": whitepaper_summary
        }
        
        output_file = os.path.join(output_dir, 'release_summary.json')
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(release_data, f, ensure_ascii=False, indent=2)
            
        print(f"Release summary successfully built at: {output_file}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
