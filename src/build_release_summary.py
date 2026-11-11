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

def scan_whitepapers(base_path):
    whitepapers = []
    try:
        for root, dirs, files in os.walk(base_path):
            for file in files:
                if 'whitepaper' in file.lower() or file.endswith('.md'):
                    full_path = os.path.join(root, file)
                    whitepapers.append(full_path)
    except Exception as e:
        print(f"Error scanning whitepapers: {e}")
    return whitepapers

def main():
    try:
        workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        repo_path = os.path.join(workspace, 'TOAI-elegant-lang')
        
        print(f"Analyzing repository at: {repo_path}")
        
        git_entries = get_git_log(repo_path)
        whitepapers = scan_whitepapers(repo_path)
        
        summary_data = {
            "timestamp": datetime.datetime.now().isoformat(),
            "git_recent_commits": git_entries,
            "detected_whitepapers": whitepapers,
            "release_status": "Generated successfully by TOAI release summary tool"
        }
        
        output_dir = os.path.join(workspace, 'TOAI_Generated')
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, 'release_summary.json')
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, ensure_ascii=False, indent=4)
            
        print(f"Release summary successfully written to {output_file}")
        
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
