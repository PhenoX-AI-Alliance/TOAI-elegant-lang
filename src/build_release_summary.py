import sys
import os
import traceback
import time
import json
import subprocess
import datetime

def get_git_log(repo_path, max_count=20):
    try:
        cmd = ["git", "-C", repo_path, "log", f"-n", str(max_count), "--pretty=format:%h - %an, %ar : %s"]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Error fetching git log: {str(e)}"]

def scan_whitepaper(repo_path):
    possible_paths = [
        os.path.join(repo_path, "WHITE_PAPER.md"),
        os.path.join(repo_path, "docs", "WHITE_PAPER.md"),
        os.path.join(repo_path, "CONSTITUTION.md")
    ]
    for p in possible_paths:
        if os.path.exists(p):
            try:
                with open(p, "r", encoding="utf-8") as f:
                    return f.read()[:1000]
            except Exception:
                pass
    return "No whitepaper found."

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_path = os.path.join(workspace_dir, 'TOAI-elegant-lang')
    
    print(f"Scanning repository at: {repo_path}")
    
    logs = get_git_log(repo_path)
    whitepaper_snippet = scan_whitepaper(repo_path)
    
    summary = {
        "timestamp": datetime.datetime.now().isoformat(),
        "repository": "TOAI-elegant-lang",
        "recent_commits": logs,
        "whitepaper_summary": whitepaper_snippet
    }
    
    output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'release_summary.json')
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
        
    print(f"Release summary successfully generated at: {output_path}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
