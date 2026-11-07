import sys
import os
import traceback
import time
import json
import subprocess
import datetime

def get_git_log():
    try:
        result = subprocess.run(
            ['git', 'log', '-n', '10', '--oneline'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except Exception as e:
        return f"Git log not available: {e}"

def scan_documents():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    docs = []
    try:
        for root, dirs, files in os.walk(workspace_dir):
            for file in files:
                if file.endswith('.md') or file.endswith('.txt'):
                    full_path = os.path.join(root, file)
                    docs.append(full_path)
    except Exception as e:
        print(f"Error scanning documents: {e}", file=sys.stderr)
    return docs

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    
    git_logs = get_git_log()
    documents = scan_documents()
    
    summary = {
        "timestamp": datetime.datetime.now().isoformat(),
        "git_recent_commits": git_logs.splitlines(),
        "scanned_document_count": len(documents),
        "sample_documents": documents[:10]
    }
    
    output_path = os.path.join(output_dir, 'release_summary.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
        
    print(f"Release summary successfully built at: {output_path}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
