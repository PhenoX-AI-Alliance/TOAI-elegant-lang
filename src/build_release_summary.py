import sys
import os
import traceback
import time
import json
import subprocess
from datetime import datetime

def run_git_log():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_path = os.path.join(workspace_dir, 'TOAI-elegant-lang')
    if not os.path.isdir(os.path.join(repo_path, '.git')):
        return "Git repository not found or not initialized."
    try:
        result = subprocess.run(
            ['git', 'log', '-n', '10', '--oneline'],
            cwd=repo_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout
    except Exception as e:
        return f"Error fetching git log: {str(e)}"

def scan_documents():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_path = os.path.join(workspace_dir, 'TOAI-elegant-lang')
    docs = []
    if os.path.exists(repo_path):
        for root, dirs, files in os.walk(repo_path):
            for file in files:
                if file.endswith('.md') or file.endswith('.txt'):
                    docs.append(os.path.join(root, file))
    return docs

def main():
    try:
        workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        output_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'src')
        os.makedirs(output_dir, exist_ok=True)
        
        git_logs = run_git_log()
        documents = scan_documents()
        
        summary = {
            "timestamp": datetime.now().isoformat(),
            "git_log": git_logs,
            "scanned_documents_count": len(documents),
            "documents": documents[:20]
        }
        
        output_file = os.path.join(output_dir, 'release_summary.json')
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=4)
        
        print(f"Successfully generated release summary at {output_file}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
