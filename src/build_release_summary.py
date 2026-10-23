import sys
import os
import subprocess
import json
from datetime import datetime

def get_git_log(max_count=10):
    try:
        repo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        if not os.path.exists(os.path.join(repo_path, ".git")):
            return "Git repository not found."
        
        result = subprocess.run(
            ["git", "log", f"-n {max_count}", "--pretty=format:%h - %an, %ar : %s"],
            cwd=repo_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except Exception as e:
        return f"Failed to retrieve git log: {e}"

def scan_whitepaper():
    try:
        repo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        whitepaper_candidates = [
            os.path.join(repo_path, "WHITE_PAPER.md"),
            os.path.join(repo_path, "docs", "WHITE_PAPER.md"),
            os.path.join(repo_path, "CONSTITUTION.md")
        ]
        
        found_info = {}
        for path in whitepaper_candidates:
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                    found_info[os.path.basename(path)] = content[:300] + "..."
        return found_info
    except Exception as e:
        return {"error": str(e)}

def main():
    print("Building release summary...")
    git_history = get_git_log()
    whitepaper_summary = scan_whitepaper()
    
    summary_data = {
        "timestamp": datetime.now().isoformat(),
        "git_log": git_history,
        "whitepaper_snippets": whitepaper_summary
    }
    
    output_dir = os.environ.get("TOAI_WORKSPACE_DIR", "/home/phenox/gemini-sandbox/")
    target_output_dir = os.path.join(output_dir, "TOAI_Generated")
    os.makedirs(target_output_dir, exist_ok=True)
    
    output_path = os.path.join(target_output_dir, "release_summary.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(summary_data, f, ensure_ascii=False, indent=2)
    
    print(f"Release summary successfully generated at: {output_path}")

if __name__ == "__main__":
    main()
