import sys
import os
import subprocess
import json
from datetime import datetime

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_path = os.path.join(workspace_dir, 'TOAI-elegant-lang')
    
    if not os.path.exists(repo_path):
        print(f"Error: Repository path not found: {repo_path}")
        sys.exit(1)
        
    os.chdir(repo_path)
    
    git_log = ""
    try:
        result = subprocess.run(
            ['git', 'log', '-n', '10', '--pretty=format:%h - %an, %ar : %s'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        git_log = result.stdout
    except subprocess.CalledProcessError as e:
        git_log = f"Could not retrieve git log: {e.stderr}"
    except Exception as e:
        git_log = f"Git log error: {str(e)}"
        
    whitepaper_path = os.path.join(repo_path, 'WHITEPAPER.md')
    whitepaper_content = ""
    if os.path.exists(whitepaper_path):
        try:
            with open(whitepaper_path, 'r', encoding='utf-8') as f:
                whitepaper_content = f.read()[:1000]
        except Exception as e:
            whitepaper_content = f"Error reading whitepaper: {str(e)}"
    else:
        whitepaper_content = "WHITEPAPER.md not found."
        
    summary_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "git_recent_commits": git_log.splitlines(),
        "whitepaper_excerpt": whitepaper_content
    }
    
    output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, 'release_summary.json')
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, indent=2, ensure_ascii=False)
        
    print(f"Release summary successfully generated at: {output_file}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)