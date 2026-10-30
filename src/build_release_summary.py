import sys
import os
import traceback
import subprocess
import json
import datetime

def get_git_log(max_count=20):
    try:
        cmd = ['git', 'log', f'-n {max_count}', '--pretty=format:%h - %an, %ar : %s']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.splitlines()
    except Exception as e:
        print(f"Warning: Could not fetch git log: {e}")
        return []

def scan_whitepaper(workspace_dir):
    whitepaper_path = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'WHITEPAPER.md')
    if os.path.exists(whitepaper_path):
        try:
            with open(whitepaper_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                return [line.strip() for line in lines[:10] if line.strip()]
        except Exception as e:
            print(f"Warning: Could not read whitepaper: {e}")
    return []

def main():
    try:
        workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        os.chdir(os.path.join(workspace_dir, 'TOAI-elegant-lang'))
        
        git_commits = get_git_log()
        whitepaper_summary = scan_whitepaper(workspace_dir)
        
        release_info = {
            "timestamp": datetime.datetime.now().isoformat(),
            "whitepaper_excerpt": whitepaper_summary,
            "recent_commits": git_commits
        }
        
        output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, 'release_summary.json')
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(release_info, f, ensure_ascii=False, indent=2)
            
        print(f"Successfully generated release summary at: {output_path}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
