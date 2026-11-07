import sys
import os
import traceback
import subprocess
import json
from datetime import datetime

def main():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_path = os.path.join(workspace, 'TOAI-elegant-lang')
    output_dir = os.path.join(workspace, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, 'release_summary.json')

    git_logs = []
    try:
        if os.path.exists(os.path.join(repo_path, '.git')):
            result = subprocess.run(
                ['git', '-C', repo_path, 'log', '-n', '10', '--pretty=format:%h - %an, %ar : %s'],
                capture_output=True,
                text=True,
                check=True
            )
            git_logs = result.stdout.splitlines()
        else:
            git_logs = ["Git repository not initialized or path not found."]
    except Exception as e:
        git_logs = [f"Failed to fetch git log: {str(e)}"]

    white_papers = []
    docs_path = os.path.join(repo_path, 'docs')
    if os.path.exists(docs_path):
        for root, dirs, files in os.walk(docs_path):
            for file in files:
                if file.endswith('.md'):
                    white_papers.append(os.path.relpath(os.path.join(root, file), repo_path))

    summary = {
        "timestamp": datetime.now().isoformat(),
        "repository": "TOAI-elegant-lang",
        "recent_commits": git_logs,
        "white_papers_and_docs": white_papers
    }

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print(f"Successfully generated release summary at: {output_file}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
