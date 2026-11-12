import sys
import os
import traceback
import time
import json
import subprocess
from datetime import datetime

def get_git_log():
    try:
        repo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        result = subprocess.run(
            ["git", "log", "-n", "10", "--pretty=format:%h - %an, %ar : %s"],
            cwd=repo_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout
    except Exception as e:
        return f"Git log retrieval failed: {str(e)}"

def scan_whitepaper():
    try:
        workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        whitepaper_path = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'docs', 'whitepaper.md')
        if os.path.exists(whitepaper_path):
            with open(whitepaper_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return content[:500] + "... [Truncated]"
        return "Whitepaper not found."
    except Exception as e:
        return f"Whitepaper scan failed: {str(e)}"

def main():
    try:
        print("Starting release summary build...")
        git_history = get_git_log()
        whitepaper_summary = scan_whitepaper()
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        summary_data = {
            "timestamp": timestamp,
            "git_log": git_history,
            "whitepaper_excerpt": whitepaper_summary
        }
        
        workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
        os.makedirs(output_dir, exist_ok=True)
        
        output_path = os.path.join(output_dir, 'release_summary.json')
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, indent=4, ensure_ascii=False)
            
        print(f"Release summary successfully generated at: {output_path}")
        
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
