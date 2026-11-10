import sys
import os
import traceback
import time
import json
import subprocess
import datetime

def get_git_logs(repo_path, max_count=20):
    try:
        cmd = ["git", "-C", repo_path, "log", f"-n", str(max_count), "--pretty=format:%h - %an: %s (%ad)", "--date=short"]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.splitlines()
    except Exception as e:
        print(f"Warning: Failed to fetch git logs: {e}")
        return []

def scan_whitepapers(base_path):
    papers = []
    try:
        for root, dirs, files in os.walk(base_path):
            for file in files:
                if file.endswith(".md") and ("whitepaper" in file.lower() or "release" in file.lower() or "doc" in file.lower()):
                    papers.append(os.path.join(root, file))
    except Exception as e:
        print(f"Warning: Failed to scan documents: {e}")
    return papers

def main():
    try:
        workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        repo_path = os.path.join(workspace_dir, 'TOAI-elegant-lang')
        
        print(f"Scanning repository at: {repo_path}")
        logs = get_git_logs(repo_path)
        papers = scan_whitepapers(repo_path)
        
        summary = {
            "timestamp": datetime.datetime.now().isoformat(),
            "git_recent_commits": logs,
            "whitepapers_found": papers
        }
        
        output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, 'release_summary.json')
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
            
        print(f"Release summary successfully generated at: {output_file}")
        
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
