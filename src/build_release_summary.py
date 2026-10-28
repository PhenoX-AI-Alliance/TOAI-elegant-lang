import sys
import os
import subprocess
import json
import datetime

def run_git_log():
    repo_path = os.environ.get('TOAI_WORKSPACE_DIR', '.')
    target_repo = os.path.join(repo_path, 'TOAI-elegant-lang')
    if not os.path.exists(os.path.join(target_repo, '.git')):
        print("Git repository not found, initializing or falling back...")
        return "No git history available (Not a git repo)"
    
    try:
        result = subprocess.run(
            ['git', '-C', target_repo, 'log', '-n', '10', '--oneline'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Git log error: {e.stderr}"

def scan_whitepapers():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '.')
    docs_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang')
    summary = []
    if os.path.exists(docs_dir):
        for root, dirs, files in os.walk(docs_dir):
            for file in files:
                if file.endswith('.md') or file.endswith('.txt'):
                    summary.append(os.path.join(root, file))
    return summary

def main():
    print("Building release summary...")
    git_logs = run_git_log()
    whitepapers = scan_whitepapers()
    
    release_data = {
        "timestamp": datetime.datetime.now().isoformat(),
        "git_recent_logs": git_logs.splitlines(),
        "scanned_documents": whitepapers
    }
    
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '.')
    output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    
    out_file = os.path.join(output_dir, 'release_summary.json')
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(release_data, f, ensure_ascii=False, indent=2)
    
    print(f"Release summary successfully generated at: {out_file}")

if __name__ == '__main__':
    main()
