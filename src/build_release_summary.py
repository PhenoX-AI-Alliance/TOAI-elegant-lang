# -*- coding: utf-8 -*-
import sys
import os
import subprocess
import datetime
import json

def get_git_log(max_count=10):
    try:
        result = subprocess.run(
            ['git', 'log', f'-n {max_count}', '--pretty=format:%h - %an, %ar : %s'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Git log retrieval failed: {str(e)}"]

def scan_whitepaper():
    whitepaper_paths = [
        "WHITEPAPER.md",
        "docs/WHITEPAPER.md",
        "CONSTITUTION.md"
    ]
    summary = {}
    for wp in whitepaper_paths:
        if os.path.exists(wp):
            try:
                with open(wp, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    summary[wp] = "".join(lines[:10]) # First 10 lines
            except Exception as e:
                summary[wp] = f"Error reading: {str(e)}"
    return summary

def main():
    print("=== TOAI Release Summary Builder ===")
    logs = get_git_log(15)
    whitepapers = scan_whitepaper()
    
    release_info = {
        "timestamp": datetime.datetime.now().isoformat(),
        "git_logs": logs,
        "whitepaper_snippets": whitepapers
    }
    
    out_file = "release_summary.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(release_info, f, ensure_ascii=False, indent=2)
        
    print(f"Release summary successfully generated at {out_file}")

if __name__ == "__main__":
    main()