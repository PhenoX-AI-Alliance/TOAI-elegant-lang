import sys
import os
import traceback
import time
import json
import subprocess
import datetime

def get_git_log():
    try:
        repo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        if not os.path.exists(os.path.join(repo_path, '.git')):
            return "Git repository not found."
        
        result = subprocess.run(
            ['git', 'log', '-n', '10', '--oneline'],
            cwd=repo_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except Exception as e:
        return f"Failed to retrieve git log: {str(e)}"

def scan_whitepapers():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    papers_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang')
    summaries = []
    try:
        if os.path.exists(papers_dir):
            for root, dirs, files in os.walk(papers_dir):
                for file in files:
                    if file.endswith('.md') or file.endswith('.txt'):
                        summaries.append(os.path.join(root, file))
    except Exception as e:
        summaries.append(f"Error scanning files: {str(e)}")
    return summaries

def main():
    try:
        print("Starting release summary generation...")
        git_log = get_git_log()
        whitepapers = scan_whitepapers()
        
        summary_data = {
            "timestamp": datetime.datetime.now().isoformat(),
            "git_recent_commits": git_log.splitlines() if isinstance(git_log, str) else [],
            "scanned_documents": whitepapers
        }
        
        workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
        os.makedirs(output_dir, exist_ok=True)
        
        output_path = os.path.join(output_dir, 'release_summary.json')
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, indent=2, ensure_ascii=False)
            
        print(f"Release summary successfully written to {output_path}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
