import sys
import os
import subprocess
import json
import datetime

def get_git_logs():
    try:
        if not os.path.exists(".git"):
            return "No git repository found in current directory."
        result = subprocess.run(
            ["git", "log", "-n", "10", "--pretty=format:%h - %an, %ar : %s"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except Exception as e:
        return f"Failed to retrieve git logs: {str(e)}"

def scan_whitepaper():
    candidates = ["whitepaper.md", "README.md", "CONSTITUTION.md"]
    found_content = {}
    for c in candidates:
        if os.path.exists(c):
            try:
                with open(c, "r", encoding="utf-8") as f:
                    found_content[c] = f.read()[:500]
            except Exception as e:
                found_content[c] = f"Error reading file: {str(e)}"
    return found_content

def main():
    print("Generating release summary...")
    git_logs = get_git_logs()
    whitepaper_data = scan_whitepaper()
    
    summary = {
        "timestamp": datetime.datetime.now().isoformat(),
        "git_logs": git_logs,
        "whitepaper_snippets": whitepaper_data
    }
    
    output_path = "release_summary.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    print(f"Successfully generated release summary at {output_path}")

if __name__ == "__main__":
    main()
