import sys
import os
import traceback
import time
import json
import subprocess
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
    try:
        for root, dirs, files in os.walk(workspace_dir):
            for file in files:
                if file.endswith('.md') or file.endswith('.txt'):
                    docs.append(os.path.join(root, file))
    except Exception as e:
        print(f"Error scanning documents: {e}", file=sys.stderr)
    return docs

def main():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    output_dir = os.path.join(workspace, 'TOAI-elegant-lang', 'releases')
    os.makedirs(output_dir, exist_ok=True)
    
    git_commits = get_git_log()
    documents = scan_documents(workspace)
    
    summary = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "version": "1.0.0",
        "recent_commits": git_commits,
        "scanned_documents_count": len(documents),
        "documents": documents[:20]
    }
    
    output_file = os.path.join(output_dir, 'release_summary.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
        
    print(f"Release summary successfully generated at: {output_file}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
