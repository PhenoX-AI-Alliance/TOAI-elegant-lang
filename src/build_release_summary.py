import sys
import os
import traceback
import time
import json
import subprocess
import datetime

def get_git_log(repo_path, max_count=20):
    try:
        cmd = ['git', '-C', repo_path, 'log', f'-n', str(max_count), '--pretty=format:%h - %an, %ar : %s']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Error fetching git log: {str(e)}"]

def scan_whitepaper(workspace_dir):
    wp_path = os.path.join(workspace_dir, 'WHITE_PAPER.md')
    if os.path.exists(wp_path):
        try:
            with open(wp_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.splitlines()
                return lines[:10]
        except Exception as e:
            return [f"Error reading WHITE_PAPER.md: {str(e)}"]
    return ["WHITE_PAPER.md not found."]

def main():
    try:
        workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        repo_path = os.path.join(workspace_dir, 'TOAI-elegant-lang')
        
        print(f"Scanning repository at: {repo_path}")
        git_logs = get_git_log(repo_path)
        
        print("Scanning whitepaper...")
        wp_summary = scan_whitepaper(workspace_dir)
        
        release_data = {
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "version": "1.0.0-release-candidate",
            "git_history": git_logs,
            "whitepaper_excerpt": wp_summary
        }
        
        output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, 'release_summary.json')
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(release_data, f, indent=2, ensure_ascii=False)
            
        print(f"Release summary successfully built at: {output_file}")
        
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
