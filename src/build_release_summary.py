import sys
import os
import traceback
import time
import json
import subprocess
import datetime

def get_git_logs(repo_path, max_count=20):
    try:
        cmd = ['git', '-C', repo_path, 'log', f'-n {max_count}', '--pretty=format:%h - %an: %s (%ad)', '--date=short']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Error fetching git logs: {str(e)}"]

def scan_whitepapers(repo_path):
    papers = []
    for root, dirs, files in os.walk(repo_path):
        for file in files:
            if 'whitepaper' in file.lower() or file.endswith('.md'):
                papers.append(os.path.join(root, file))
    return papers

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_path = os.path.join(workspace_dir, 'TOAI-elegant-lang')
    
    logs = get_git_logs(repo_path)
    papers = scan_whitepapers(repo_path)
    
    summary = {
        "timestamp": datetime.datetime.now().isoformat(),
        "recent_commits": logs,
        "related_documents": papers
    }
    
    output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'release_summary.json')
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
        
    print(f"Successfully generated release summary at: {output_path}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
