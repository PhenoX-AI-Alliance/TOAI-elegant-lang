# -*- coding: utf-8 -*-
import sys
import os
import traceback
import subprocess
import json
import datetime

def run_git_log():
    repo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    if not os.path.exists(os.path.join(repo_path, ".git")):
        return "Git repository not found or not initialized."
    try:
        result = subprocess.run(
            ["git", "log", "-n", "10", "--oneline"],
            cwd=repo_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Error running git log: {e.stderr}"

def scan_whitepapers():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    search_dirs = [
        workspace,
        os.path.join(workspace, 'TOAI-elegant-lang'),
        os.path.join(workspace, 'TOAI_Generated')
    ]
    found_files = []
    for d in search_dirs:
        if os.path.exists(d):
            for root, dirs, files in os.walk(d):
                for file in files:
                    if "whitepaper" in file.lower() or "summary" in file.lower() or "release" in file.lower():
                        found_files.append(os.path.join(root, file))
    return found_files

def main():
    try:
        print("=== TOAI Release Summary Generator ===")
        git_logs = run_git_log()
        whitepapers = scan_whitepapers()
        
        summary = {
            "timestamp": datetime.datetime.now().isoformat(),
            "git_recent_commits": git_logs.splitlines(),
            "related_documents": whitepapers
        }
        
        workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        output_dir = os.path.join(workspace, 'TOAI_Generated')
        os.makedirs(output_dir, exist_ok=True)
        
        output_path = os.path.join(output_dir, 'release_summary.json')
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=4)
            
        print(f"Successfully generated release summary at: {output_path}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
