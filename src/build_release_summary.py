import sys
import os
import traceback
import time
import json
import subprocess
import datetime

def get_git_log(repo_path, max_count=20):
    try:
        cmd = ['git', '-C', repo_path, 'log', f'-n {max_count}', '--pretty=format:%h - %an, %ar : %s']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Error fetching git log: {str(e)}"]

def scan_whitepapers(base_path):
    papers = []
    try:
        for root, dirs, files in os.walk(base_path):
            for file in files:
                if file.endswith('.md') and ('whitepaper' in file.lower() or 'doc' in file.lower()):
                    papers.append(os.path.join(root, file))
    except Exception as e:
        pass
    return papers

def main():
    try:
        workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        repo_path = os.path.join(workspace_dir, 'TOAI-elegant-lang')
        
        if not os.path.exists(repo_path):
            os.makedirs(repo_path, exist_ok=True)
            try:
                subprocess.run(['git', 'init', repo_path], check=True)
            except Exception:
                pass
                
        git_logs = get_git_log(repo_path)
        whitepapers = scan_whitepapers(workspace_dir)
        
        summary = {
            "timestamp": datetime.datetime.now().isoformat(),
            "git_recent_commits": git_logs,
            "detected_documents": whitepapers,
            "version": "1.0.0"
        }
        
        output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
        os.makedirs(output_dir, exist_ok=True)
        
        out_file = os.path.join(output_dir, 'release_summary.json')
        with open(out_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
            
        print(f"Release summary successfully generated at {out_file}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
