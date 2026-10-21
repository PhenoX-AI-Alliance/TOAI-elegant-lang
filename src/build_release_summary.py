import sys
import os
import subprocess
import json
from datetime import datetime

def get_git_log(max_count=10):
    repo_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    if not os.path.exists(os.path.join(repo_dir, '.git')):
        return ["Git repository not initialized."]
    try:
        cmd = ['git', 'log', f'-n {max_count}', '--pretty=format:%h - %an, %ar : %s']
        result = subprocess.run(cmd, cwd=repo_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Error fetching git log: {str(e)}"]

def scan_whitepapers():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    papers = []
    search_paths = [
        workspace,
        os.path.join(workspace, 'TOAI-elegant-lang'),
        os.path.join(workspace, 'TOAI_Generated')
    ]
    for path in search_paths:
        if os.path.exists(path):
            for root, dirs, files in os.walk(path):
                for file in files:
                    if 'whitepaper' in file.lower() or 'summary' in file.lower() or file.endswith('.md'):
                        papers.append(os.path.join(root, file))
    return papers

def main():
    print("Generating release summary...")
    logs = get_git_log()
    papers = scan_whitepapers()
    
    summary = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "git_logs": logs,
        "discovered_documents": papers[:20]
    }
    
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    output_dir = os.path.join(workspace, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    
    output_path = os.path.join(output_dir, 'release_summary.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
        
    print(f"Release summary successfully written to {output_path}")

if __name__ == '__main__':
    main()
