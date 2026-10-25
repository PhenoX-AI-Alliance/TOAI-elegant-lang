#!/usr/bin/env python3
import sys
import os
import subprocess
import json
import datetime
import traceback

def run_git_log():
    repo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    if not os.path.exists(os.path.join(repo_path, ".git")):
        return "Git repository not found."
    try:
        result = subprocess.run(
            ["git", "log", "-n", "10", "--pretty=format:%h - %an: %s (%ad)"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except Exception as e:
        return f"Failed to retrieve git log: {e}"

def scan_whitepapers():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    papers = []
    try:
        for root, dirs, files in os.walk(workspace):
            for file in files:
                if "whitepaper" in file.lower() or file.endswith(".md"):
                    papers.append(os.path.join(root, file))
    except Exception as e:
        print(f"Error scanning whitepapers: {e}")
    return papers[:20]

def main():
    try:
        print("Starting Release Summary Build...")
        git_history = run_git_log()
        whitepapers = scan_whitepapers()
        
        summary = {
            "timestamp": datetime.datetime.now().isoformat(),
            "git_recent_commits": git_history.splitlines(),
            "scanned_documents_count": len(whitepapers),
            "sample_documents": whitepapers[:5]
        }
        
        output_dir = os.path.join(os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/'), 'TOAI_Generated')
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, 'release_summary.json')
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
            
        print(f"Release summary successfully generated at {output_file}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
