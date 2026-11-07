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
        print(f"Warning: Could not retrieve git log: {e}")
        return []

def scan_whitepaper(workspace_path):
    whitepaper_files = []
    try:
        for root, dirs, files in os.walk(workspace_path):
            for file in files:
                if 'whitepaper' in file.lower() or 'doc' in file.lower() or file.endswith('.md'):
                    whitepaper_files.append(os.path.join(root, file))
    except Exception as e:
        print(f"Warning: Could not scan documentation: {e}")
    return whitepaper_files

def main():
    try:
        workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        repo_path = os.path.join(workspace, 'TOAI-elegant-lang')
        
        print("Scanning Git repository and documentation...")
        git_commits = get_git_log(repo_path, max_count=30)
        docs = scan_whitepaper(workspace)
        
        summary_data = {
            "timestamp": datetime.datetime.now().isoformat(),
            "repository": "TOAI-elegant-lang",
            "recent_commits": git_commits,
            "associated_docs_count": len(docs),
            "status": "RELEASE_SUMMARY_BUILT_SUCCESSFULLY"
        }
        
        output_dir = os.path.join(workspace, 'TOAI_Generated')
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, 'release_summary.json')
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, ensure_ascii=False, indent=2)
            
        print(f"Release summary successfully generated at: {output_path}")
        
    except Exception as e:
        print(f"Error in release summary build: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
