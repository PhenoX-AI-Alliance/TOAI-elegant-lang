import sys
import os
import traceback
import subprocess
import json
from datetime import datetime

def run_git_log():
    try:
        repo_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        if not os.path.exists(os.path.join(repo_dir, '.git')):
            return "Git repository not found."
        
        result = subprocess.run(
            ['git', 'log', '-n', '10', '--oneline'],
            cwd=repo_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout
    except Exception as e:
        return f"Failed to retrieve git log: {str(e)}"

def scan_documents():
    docs = []
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    search_path = os.path.join(workspace, 'TOAI-elegant-lang')
    if os.path.exists(search_path):
        for root, dirs, files in os.walk(search_path):
            for file in files:
                if file.endswith('.md'):
                    docs.append(os.path.join(root, file))
    return docs

def main():
    try:
        print("Starting release summary generation...")
        git_log_output = run_git_log()
        markdown_files = scan_documents()
        
        summary = {
            "timestamp": datetime.now().isoformat(),
            "git_recent_commits": git_log_output.splitlines(),
            "documentation_files_scanned": markdown_files
        }
        
        output_dir = os.path.join(os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/'), 'TOAI_Generated')
        os.makedirs(output_dir, exist_ok=True)
        
        output_file = os.path.join(output_dir, 'release_summary.json')
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
            
        print(f"Release summary successfully written to {output_file}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
