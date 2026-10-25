import sys
import os
import subprocess
import json
import glob
from datetime import datetime

def main():
    repo_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    os.chdir(repo_dir)
    
    git_logs = []
    try:
        result = subprocess.run(['git', 'log', '-n', '10', '--oneline'], capture_output=True, text=True, check=True)
        git_logs = result.stdout.strip().split('\n')
    except Exception as e:
        git_logs = [f"Git log unavailable: {str(e)}"]
        
    white_papers = []
    wp_pattern = os.path.join(repo_dir, '**', '*.md')
    for file_path in glob.glob(wp_pattern, recursive=True):
        if 'node_modules' in file_path or '.git' in file_path:
            continue
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                first_line = f.readline().strip()
                white_papers.append({
                    'path': os.path.relpath(file_path, repo_dir),
                    'title': first_line if first_line else 'No Title'
                })
        except Exception:
            pass
            
    summary = {
        'generated_at': datetime.utcnow().isoformat() + 'Z',
        'recent_commits': git_logs,
        'documents_scanned': len(white_papers),
        'documents': white_papers[:20]
    }
    
    output_path = os.path.join(repo_dir, 'RELEASE_SUMMARY.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
        
    print(f"Successfully generated release summary at: {output_path}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"Error in build_release_summary: {e}", file=sys.stderr)
        sys.exit(1)
