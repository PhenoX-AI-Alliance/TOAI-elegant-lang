import sys
import os
import traceback
import time
import json
import subprocess
import datetime

def get_git_log(repo_path, max_count=20):
    try:
        cmd = ['git', '-C', repo_path, 'log', f'-n', str(max_count), '--pretty=format:%h - %an: %s (%ad)']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Git log retrieval failed: {str(e)}"]

def scan_whitepapers(workspace_path):
    whitepaper_files = []
    try:
        for root, dirs, files in os.walk(workspace_path):
            for file in files:
                if 'whitepaper' in file.lower() or 'release' in file.lower() or file.endswith('.md'):
                    whitepaper_files.append(os.path.join(root, file))
    except Exception as e:
        pass
    return whitepaper_files

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_path = os.path.join(workspace_dir, 'TOAI-elegant-lang')
    
    print("Scanning git repository and documentation...")
    git_logs = get_git_log(repo_path)
    whitepapers = scan_whitepapers(workspace_dir)
    
    summary_data = {
        "timestamp": datetime.datetime.now().isoformat(),
        "git_logs": git_logs,
        "whitepapers_found": whitepapers[:10]
    }
    
    output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'release_summary.json')
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, ensure_ascii=False, indent=2)
        
    print(f"Release summary successfully generated at: {output_path}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
