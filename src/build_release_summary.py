import sys
import os
import traceback
import subprocess
import json
from datetime import datetime

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_path = os.path.join(workspace_dir, 'TOAI-elegant-lang')
    
    summary_data = {
        "timestamp": datetime.now().isoformat(),
        "git_log": [],
        "whitepaper_summary": "No whitepaper found."
    }
    
    try:
        if os.path.isdir(os.path.join(repo_path, '.git')):
            result = subprocess.run(
                ['git', 'log', '-n', '10', '--oneline'],
                cwd=repo_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )
            summary_data["git_log"] = result.stdout.splitlines()
        else:
            summary_data["git_log"] = ["Not a git repository or git not initialized."]
    except Exception as e:
        summary_data["git_log"] = [f"Error fetching git log: {str(e)}"]
        
    whitepaper_path = os.path.join(repo_path, 'WHITEPAPER.md')
    if os.path.exists(whitepaper_path):
        try:
            with open(whitepaper_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                summary_data["whitepaper_summary"] = "".join(lines[:20])
        except Exception as e:
            summary_data["whitepaper_summary"] = f"Error reading whitepaper: {str(e)}"
            
    output_path = os.path.join(workspace_dir, 'TOAI_Generated', 'release_summary.json')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, ensure_ascii=False, indent=2)
        
    print(f"Successfully generated release summary at: {output_path}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
