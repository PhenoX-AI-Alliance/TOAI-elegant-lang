import sys
import os
import subprocess
import json
from datetime import datetime

def get_git_log():
    try:
        result = subprocess.run(
            ['git', 'log', '-n', '10', '--pretty=format:%h - %an, %ar : %s'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
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
        pass
    return docs[:20]

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    
    summary = {
        "timestamp": datetime.now().isoformat(),
        "git_logs": get_git_log(),
        "scanned_documents": scan_documents(workspace_dir)
    }
    
    out_file = os.path.join(output_dir, 'release_summary.json')
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    print(f"Release summary successfully generated at: {out_file}")

if __name__ == '__main__':
    main()
