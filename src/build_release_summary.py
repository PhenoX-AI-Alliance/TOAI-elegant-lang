# -*- coding: utf-8 -*-
import sys
import os
import subprocess
import json
import datetime

def get_git_log(max_count=20):
    try:
        repo_path = os.path.dirname(os.path.abspath(__file__))
        cmd = ["git", "-C", repo_path, "log", f"-n {max_count}", "--pretty=format:%h - %an, %ar : %s"]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Git log retrieval failed: {str(e)}"]

def scan_whitepapers():
    docs = []
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        target = os.path.join(base_dir, "..")
        for root, dirs, files in os.walk(target):
            for file in files:
                if file.endswith(".md") or file.endswith(".txt"):
                    docs.append(os.path.join(root, file))
    except Exception as e:
        pass
    return docs

def generate_summary():
    logs = get_git_log(15)
    papers = scan_whitepapers()
    
    summary = {
        "timestamp": datetime.datetime.now().isoformat(),
        "version": "1.0.0-gaia",
        "recent_commits": logs,
        "scanned_documents_count": len(papers)
    }
    
    out_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "release_summary.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    print(f"Release summary successfully generated at: {out_file}")

if __name__ == "__main__":
    generate_summary()
