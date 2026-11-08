import sys
import os
import traceback
import subprocess
import json
from datetime import datetime

def get_git_log():
    try:
        result = subprocess.run(
            ['git', 'log', '-n', '10', '--pretty=format:%h - %an, %ar : %s'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Git log unavailable: {str(e)}"]

def scan_documents(workspace_dir):
    docs = []
    whitepaper_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang')
    if os.path.exists(whitepaper_dir):
        for root, dirs, files in os.walk(whitepaper_dir):
            for file in files:
                if file.endswith('.md') or file.endswith('.txt'):
                    docs.append(os.path.join(root, file))
    return docs

def main():
    try:
        workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
        os.makedirs(output_dir, exist_ok=True)
        
        git_history = get_git_log()
        documents = scan_documents(workspace_dir)
        
        summary = {
            "timestamp": datetime.now().isoformat(),
            "git_recent_commits": git_history,
            "scanned_documents_count": len(documents),
            "scanned_documents": documents[:20],
            "status": "success"
        }
        
        output_file = os.path.join(output_dir, 'release_summary.json')
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
            
        print(f"Release summary successfully generated at: {output_file}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
