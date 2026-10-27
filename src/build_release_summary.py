import sys
import os
import traceback
import subprocess
import json
import datetime
import glob

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_path = os.path.join(workspace_dir, 'TOAI-elegant-lang')
    
    git_log = []
    try:
        if os.path.exists(os.path.join(repo_path, '.git')):
            result = subprocess.run(
                ['git', '-C', repo_path, 'log', '-n', '10', '--oneline'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )
            git_log = result.stdout.strip().split('\n')
        else:
            git_log = ["No git repository initialized or found at " + repo_path]
    except Exception as e:
        git_log = [f"Error fetching git log: {str(e)}"]

    whitepaper_docs = []
    try:
        search_pattern = os.path.join(workspace_dir, '**', '*.md')
        for file_path in glob.glob(search_pattern, recursive=True):
            if 'whitepaper' in file_path.lower() or 'constitution' in file_path.lower() or 'readme' in file_path.lower():
                whitepaper_docs.append(file_path)
    except Exception as e:
        whitepaper_docs = [f"Error scanning documents: {str(e)}"]

    summary_data = {
        "timestamp": datetime.datetime.now().isoformat(),
        "version": "1.0.0",
        "git_recent_commits": git_log,
        "related_whitepapers": whitepaper_docs,
        "ecosystem": "Gaia Ecosystem - Earth of Life"
    }

    output_file = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'release_summary.json')
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, ensure_ascii=False, indent=2)
        
    print(f"Release summary successfully generated at: {output_file}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
