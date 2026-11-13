import sys
import os
import traceback
import time
import json
import subprocess
from datetime import datetime

def get_git_logs():
    try:
        result = subprocess.run(
            ['git', 'log', '-n', '20', '--pretty=format:%h - %an, %ar : %s'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Git log retrieval failed: {str(e)}"]

def scan_workspace_docs(workspace_dir):
    docs = []
    try:
        for root, dirs, files in os.walk(workspace_dir):
            if '.git' in root or 'TOAI_Generated' in root:
                continue
            for file in files:
                if file.endswith('.md') or file.endswith('.txt') or file.endswith('.json'):
                    docs.append(os.path.join(root, file))
    except Exception as e:
        print(f"Error scanning docs: {e}", file=sys.stderr)
    return docs

def main():
    try:
        workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
        os.makedirs(output_dir, exist_ok=True)
        
        git_logs = get_git_logs()
        docs = scan_workspace_docs(workspace_dir)
        
        summary = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "version": "1.0.0",
            "git_recent_commits": git_logs,
            "scanned_documents_count": len(docs),
            "scanned_documents": docs[:50]
        }
        
        output_file = os.path.join(output_dir, 'release_summary.json')
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
            
        print(f"Release summary successfully built at: {output_file}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
