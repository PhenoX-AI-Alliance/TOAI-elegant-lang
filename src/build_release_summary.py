# -*- coding: utf-8 -*-
import sys
import os
import traceback
import time
import json
import subprocess
from datetime import datetime

def get_git_log():
    try:
        result = subprocess.run(
            ["git", "log", "-n", "10", "--pretty=format:%h - %an: %s (%ad)"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.strip().split("\n")
    except Exception as e:
        return [f"Git log retrieval failed: {str(e)}"]

def scan_workspace():
    workspace_dir = os.environ.get("TOAI_WORKSPACE_DIR", "/home/phenox/gemini-sandbox/")
    summary_path = os.path.join(workspace_dir, "TOAI_Generated", "release_summary.json")
    
    git_commits = get_git_log()
    
    release_data = {
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0-gaia",
        "git_recent_commits": git_commits,
        "ecosystem": "Earth of Life (Gaia Ecosystem)"
    }
    
    try:
        with open(summary_path, "w", encoding="utf-8") as f:
            json.dump(release_data, f, ensure_ascii=False, indent=2)
        print(f"Successfully generated release summary at: {summary_path}")
    except Exception as e:
        print(f"Failed to write release summary: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    try:
        scan_workspace()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
