# -*- coding: utf-8 -*-
import sys
import os
import subprocess
import datetime
import json

def get_git_log(max_count=10):
    try:
        repo_path = os.path.dirname(os.path.abspath(__file__))
        cmd = ["git", "-C", repo_path, "log", f"-n", str(max_count), "--oneline"]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip().splitlines()
    except Exception as e:
        return [f"Git log acquisition failed: {str(e)}"]

def scan_whitepaper():
    try:
        repo_path = os.path.dirname(os.path.abspath(__file__))
        workspace = os.path.abspath(os.path.join(repo_path, "..", ".."))
        whitepaper_candidates = [
            os.path.join(workspace, "WHITE_PAPER.md"),
            os.path.join(workspace, "CONSTITUTION.md"),
            os.path.join(repo_path, "WHITE_PAPER.md")
        ]
        for path in whitepaper_candidates:
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    return "".join(lines[:20])
        return "Whitepaper not found."
    except Exception as e:
        return f"Whitepaper scan failed: {str(e)}"

def generate_summary():
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    git_logs = get_git_log(15)
    whitepaper_snippet = scan_whitepaper()
    
    summary = {
        "timestamp": timestamp,
        "git_recent_commits": git_logs,
        "whitepaper_overview": whitepaper_snippet
    }
    
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "release_summary.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    print(f"Release summary successfully generated at: {output_path}")

if __name__ == "__main__":
    generate_summary()
