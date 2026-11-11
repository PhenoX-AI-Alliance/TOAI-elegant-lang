import sys
import os
import traceback
import time
import json
import subprocess
import datetime

def get_git_log():
    try:
        cmd = ["git", "log", "-n", "20", "--pretty=format:%h - %an, %ar : %s"]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True, encoding="utf-8")
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Git log retrieval failed: {str(e)}"]

def scan_whitepaper(workspace_dir):
    whitepaper_paths = [
        os.path.join(workspace_dir, "TOAI-elegant-lang", "WHITEPAPER.md"),
        os.path.join(workspace_dir, "WHITEPAPER.md")
    ]
    for path in whitepaper_paths:
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    return f.read()[:2000] # return first 2000 chars as summary
            except Exception:
                pass
    return "Whitepaper not found."

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    
    git_logs = get_git_log()
    whitepaper_summary = scan_whitepaper(workspace_dir)
    
    release_data = {
        "timestamp": datetime.datetime.now().isoformat(),
        "version": "v1.0.0-release",
        "recent_commits": git_logs,
        "whitepaper_excerpt": whitepaper_summary
    }
    
    output_file = os.path.join(output_dir, "release_summary.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(release_data, f, ensure_ascii=False, indent=4)
    
    print(f"Successfully generated release summary at: {output_file}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
