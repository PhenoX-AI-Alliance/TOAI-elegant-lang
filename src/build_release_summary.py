import sys
import os
import traceback
import subprocess
import json
from datetime import datetime

def run_git_log(repo_path, max_count=20):
    try:
        cmd = ["git", "-C", repo_path, "log", f"-n", str(max_count), "--pretty=format:%h - %an, %ar : %s"]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.splitlines()
    except Exception as e:
        print(f"Warning: Could not fetch git log: {e}")
        return []

def scan_whitepapers(repo_path):
    papers = []
    for root, dirs, files in os.walk(repo_path):
        for file in files:
            if "whitepaper" in file.lower() or file.endswith(".md"):
                papers.append(os.path.join(root, file))
    return papers

def main():
    try:
        workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        repo_path = os.path.join(workspace, 'TOAI-elegant-lang')
        
        if not os.path.exists(repo_path):
            os.makedirs(repo_path, exist_ok=True)
            try:
                subprocess.run(["git", "init", repo_path], check=True)
            except Exception as e:
                print(f"Git init notice: {e}")

        git_logs = run_git_log(repo_path)
        whitepapers = scan_whitepapers(repo_path)

        summary = {
            "timestamp": datetime.utcnow().isoformat(),
            "git_recent_commits": git_logs,
            "whitepapers_found": whitepapers,
            "status": "success"
        }

        output_dir = os.path.join(workspace, 'TOAI_Generated')
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, 'release_summary.json')

        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)

        print(f"Release summary successfully generated at: {output_path}")

    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
