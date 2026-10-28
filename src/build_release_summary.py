import sys
import os
import subprocess
import json
from datetime import datetime

def get_git_log(max_count=10):
    try:
        result = subprocess.run(
            ["git", "log", f"-n", str(max_count), "--pretty=format:%h - %an: %s (%ad)"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Git log unavailable: {str(e)}"]

def scan_whitepaper():
    base_dir = os.environ.get("TOAI_WORKSPACE_DIR", "/home/phenox/gemini-sandbox/")
    possible_paths = [
        os.path.join(base_dir, "WHITEPAPER.md"),
        os.path.join(base_dir, "CONSTITUTION.md"),
        os.path.join(base_dir, "README.md")
    ]
    summary = {}
    for path in possible_paths:
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    summary[os.path.basename(path)] = "".join(lines[:10])
            except Exception as e:
                summary[os.path.basename(path)] = f"Error reading file: {str(e)}"
    return summary

def main():
    print("Generating release summary...")
    logs = get_git_log()
    whitepapers = scan_whitepaper()
    
    release_data = {
        "timestamp": datetime.now().isoformat(),
        "git_recent_commits": logs,
        "documentation_snippets": whitepapers
    }
    
    output_dir = os.environ.get("TOAI_WORKSPACE_DIR", "/home/phenox/gemini-sandbox/")
    output_file = os.path.join(output_dir, "TOAI_Generated", "release_summary.json")
    
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(release_data, f, ensure_ascii=False, indent=2)
        
    print(f"Release summary successfully generated at: {output_file}")

if __name__ == "__main__":
    main()
