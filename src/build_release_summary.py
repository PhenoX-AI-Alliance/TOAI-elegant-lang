import sys
import os
import traceback
import time
import json
import subprocess
import datetime

def get_git_log(repo_path, max_count=20):
    try:
        result = subprocess.run(
            ['git', '-C', repo_path, 'log', f'-n {max_count}', '--pretty=format:%h - %an, %ar : %s'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except Exception as e:
        return f"Could not retrieve git log: {str(e)}"

def scan_whitepapers(repo_path):
    whitepaper_files = []
    try:
        for root, dirs, files in os.walk(repo_path):
            for file in files:
                if 'whitepaper' in file.lower() or file.endswith('.md'):
                    whitepaper_files.append(os.path.join(root, file))
    except Exception as e:
        print(f"Error scanning files: {e}", file=sys.stderr)
    return whitepaper_files

def main():
    try:
        workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        repo_path = os.path.join(workspace_dir, 'TOAI-elegant-lang')
        
        if not os.path.exists(repo_path):
            os.makedirs(repo_path, exist_ok=True)
            subprocess.run(['git', 'init', repo_path], check=True)
        
        git_log = get_git_log(repo_path)
        whitepapers = scan_whitepapers(repo_path)
        
        summary_data = {
            "timestamp": datetime.datetime.now().isoformat(),
            "git_log": git_log,
            "whitepapers_found": whitepapers,
            "version": "1.0.0"
        }
        
        output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, 'release_summary.json')
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, ensure_ascii=False, indent=4)
            
        print(f"Release summary successfully generated at: {output_path}")
        
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
