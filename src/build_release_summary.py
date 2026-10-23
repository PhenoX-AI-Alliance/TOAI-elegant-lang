# -*- coding: utf-8 -*-
import sys
import os
import subprocess
import datetime
import json

def get_git_log(max_count=20):
    try:
        repo_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        if not os.path.exists(os.path.join(repo_dir, '.git')):
            return "Git repository not initialized."
        cmd = ["git", "log", f"-n", str(max_count), "--pretty=format:%h - %an, %ar : %s"]
        result = subprocess.run(cmd, cwd=repo_dir, capture_output=True, text=True, check=True)
        return result.stdout
    except Exception as e:
        return f"Failed to retrieve git log: {str(e)}"

def scan_whitepaper():
    try:
        repo_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        whitepaper_path = os.path.join(repo_dir, 'WHITEPAPER.md')
        if os.path.exists(whitepaper_path):
            with open(whitepaper_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            return "".join(lines[:30])
        return "WHITEPAPER.md not found."
    except Exception as e:
        return f"Failed to read whitepaper: {str(e)}"

def main():
    print("Generating Release Summary for TOAI Ecosystem...")
    git_history = get_git_log(15)
    whitepaper_snippet = scan_whitepaper()
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    summary = f"""# TOAI Release Summary
Generated at: {timestamp}

## Whitepaper Overview (Snippet)
{whitepaper_snippet}

## Recent Change Log
{git_history}
"""
    
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    output_file = os.path.join(workspace_dir, 'TOAI_Generated', 'RELEASE_SUMMARY.md')
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(summary)
        
    print(f"Release summary successfully written to {output_file}")

if __name__ == '__main__':
    main()
