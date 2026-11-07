import sys
import os
import traceback
import time
import json
import subprocess
from datetime import datetime

def run_git_log():
    try:
        repo_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        if not os.path.exists(os.path.join(repo_dir, '.git')):
            return "Git repository not found at target path."
        
        result = subprocess.run(
            ['git', 'log', '-n', '10', '--pretty=format:%h - %an, %ar : %s'],
            cwd=repo_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout
    except Exception as e:
        return f"Could not retrieve git log: {str(e)}"

def generate_summary():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    output_dir = os.path.join(workspace, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    
    log_output = run_git_log()
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    summary_data = {
        "title": "TOAI Elegant Lang Release Summary",
        "generated_at": timestamp,
        "recent_commits": log_output.splitlines() if log_output else []
    }
    
    output_file = os.path.join(output_dir, 'release_summary.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, indent=2, ensure_ascii=False)
        
    md_file = os.path.join(output_dir, 'release_summary.md')
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(f"# Release Summary\n\nGenerated at: {timestamp}\n\n## Recent Commits\n")
        for commit in summary_data["recent_commits"]:
            f.write(f"- {commit}\n")
            
    print(f"Successfully generated release summaries at {output_dir}")

if __name__ == '__main__':
    try:
        generate_summary()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
