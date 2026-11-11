#!/usr/bin/env python3
import sys
import os
import subprocess
import datetime
import json

def main():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_path = os.path.join(workspace, 'TOAI-elegant-lang')
    
    if not os.path.exists(repo_path):
        print(f"Error: Repository path does not exist: {repo_path}")
        sys.exit(1)
        
    os.chdir(repo_path)
    
    git_log = ""
    try:
        result = subprocess.run(
            ['git', 'log', '-n', '10', '--oneline'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        git_log = result.stdout
    except subprocess.CalledProcessError as e:
        git_log = f"Failed to fetch git log: {e.stderr}"
    except Exception as e:
        git_log = f"Git log error: {str(e)}"
        
    whitepaper_path = os.path.join(repo_path, 'WHITEPAPER.md')
    whitepaper_content = "Whitepaper not found."
    if os.path.exists(whitepaper_path):
        with open(whitepaper_path, 'r', encoding='utf-8') as f:
            whitepaper_content = f.read()[:1000]
            
    summary = {
        "timestamp": datetime.datetime.now().isoformat(),
        "recent_commits": git_log.splitlines(),
        "whitepaper_excerpt": whitepaper_content
    }
    
    output_path = os.path.join(repo_path, 'release_summary.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
        
    print(f"Release summary successfully generated at: {output_path}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"Critical error: {e}", file=sys.stderr)
        sys.exit(1)
