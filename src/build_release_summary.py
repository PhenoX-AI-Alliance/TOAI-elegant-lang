import sys
import os
import subprocess
import json
from datetime import datetime

def run_git_log():
    try:
        result = subprocess.run(
            ['git', 'log', '-n', '10', '--oneline'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        
        return result.stdout.strip().split('\n')
    except Exception as e:
        print(f"Warning: Could not fetch git log: {e}")
        return []

def scan_whitepapers():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    docs_dir = os.path.join(workspace, 'TOAI-elegant-lang', 'docs')
    papers = []
    if os.path.exists(docs_dir):
        for root, dirs, files in os.walk(docs_dir):
            for file in files:
                if file.endswith('.md'):
                    papers.append(os.path.join(root, file))
    return papers

def main():
    print("Initializing Release Summary Builder...")
    logs = run_git_log()
    papers = scan_whitepapers()
    
    summary = {
        "timestamp": datetime.now().isoformat(),
        "recent_commits": logs,
        "whitepapers_found": papers,
        "version": "1.0.0"
    }
    
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    output_dir = os.path.join(workspace, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'release_summary.json')
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
        
    print(f"Release summary successfully generated at: {output_path}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"Error in release summary build: {e}")
        sys.exit(1)
