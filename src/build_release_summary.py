# -*- coding: utf-8 -*-
import sys
import os
import subprocess
import datetime
import json

def get_git_log(max_count=10):
    try:
        repo_path = os.path.dirname(os.path.abspath(__file__))
        cmd = ["git", "-C", repo_path, "log", f"-n{max_count}", "--pretty=format:%h - %an: %s (%ad)"]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Git log retrieval failed: {str(e)}"]

def scan_whitepaper():
    try:
        repo_path = os.path.dirname(os.path.abspath(__file__))
        potential_paths = [
            os.path.join(repo_path, "..", "WHITE_PAPER.md"),
            os.path.join(repo_path, "WHITE_PAPER.md"),
            os.path.join(repo_path, "..", "..", "WHITE_PAPER.md")
        ]
        for path in potential_paths:
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    return f.read()[:1000] # Return summary snippet
        return "Whitepaper not found."
    except Exception as e:
        return f"Whitepaper scan failed: {str(e)}"

def build_summary():
    now = datetime.datetime.now().isoformat()
    logs = get_git_log()
    whitepaper_snippet = scan_whitepaper()
    
    summary = {
        "timestamp": now,
        "version": "1.0.0",
        "git_history": logs,
        "whitepaper_summary": whitepaper_snippet
    }
    
    output_path = os.path.join(os.path.dirname(__file__), "release_summary.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    print(f"Release summary successfully generated at: {output_path}")

if __name__ == "__main__":
    build_summary()
