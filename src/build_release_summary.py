import sys
import os
import traceback
import time
import json
import subprocess
import datetime

def get_git_logs(repo_path, max_count=20):
    try:
        cmd = ['git', '-C', repo_path, 'log', f'-n {max_count}', '--pretty=format:%h - %an, %ar : %s']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.splitlines()
    except Exception as e:
        print(f"Warning: Failed to fetch git logs: {e}")
        return []

def scan_whitepapers(repo_path):
    papers = []
    try:
        for root, dirs, files in os.walk(repo_path):
            for file in files:
                if 'whitepaper' in file.lower() or file.endswith('.md'):
                    full_path = os.path.join(root, file)
                    papers.append(full_path)
    except Exception as e:
        print(f"Warning: Failed to scan whitepapers: {e}")
    return papers

def main():
    try:
        workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        repo_path = os.path.join(workspace, 'TOAI-elegant-lang')
        
        if not os.path.isdir(repo_path):
            print(f"Error: Repository path not found: {repo_path}")
            sys.exit(1)
            
        print(f"Scanning repository at: {repo_path}")
        logs = get_git_logs(repo_path)
        papers = scan_whitepapers(repo_path)
        
        summary = {
            "generated_at": datetime.datetime.now().isoformat(),
            "repository": repo_path,
            "recent_commits": logs,
            "whitepaper_candidates": papers
        }
        
        output_dir = os.path.join(workspace, 'TOAI_Generated')
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, 'release_summary.json')
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
            
        print(f"Release summary successfully built at: {output_file}")
        
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
