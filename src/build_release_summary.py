# -*- coding: utf-8 -*-
import sys
import os
import subprocess
import json
import datetime

def get_git_log():
    try:
        if not os.path.exists('.git'):
            return "No git repository found in current directory."
        result = subprocess.run(
            ['git', 'log', '-n', '10', '--oneline'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except Exception as e:
        return f"Failed to retrieve git log: {e}"

def scan_whitepaper():
    whitepaper_path = "WHITEPAPER.md"
    if os.path.exists(whitepaper_path):
        try:
            with open(whitepaper_path, "r", encoding="utf-8") as f:
                content = f.read(500)
            return content
        except Exception as e:
            return f"Error reading WHITEPAPER.md: {e}"
    return "WHITEPAPER.md not found."

def main():
    print("Building Release Summary...")
    git_logs = get_git_log()
    whitepaper_snippet = scan_whitepaper()
    
    summary = {
        "timestamp": datetime.datetime.now().isoformat(),
        "git_recent_commits": git_logs.splitlines(),
        "whitepaper_snippet": whitepaper_snippet
    }
    
    output_filename = "release_summary.json"
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    print(f"Release summary successfully generated at {output_filename}")

if __name__ == "__main__":
    main()
