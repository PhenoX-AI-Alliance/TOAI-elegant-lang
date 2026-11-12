import sys
import os
import traceback
import time
import json
import subprocess
from datetime import datetime

def get_git_log():
    try:
        repo_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        result = subprocess.run(
            ['git', 'log', '-n', '20', '--oneline'],
            cwd=repo_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.strip().split('\n')
    except Exception as e:
        return [f"Git log retrieval failed: {str(e)}"]

def scan_whitepapers():
    try:
        repo_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        docs = []
        for root, dirs, files in os.walk(repo_dir):
            for file in files:
                if 'whitepaper' in file.lower() or file.endswith('.md'):
                    docs.append(os.path.join(root, file))
        return docs
    except Exception as e:
        return [f"Whitepaper scan failed: {str(e)}"]

def main():
    try:
        print("Starting release summary generation...")
        git_logs = get_git_log()
        whitepapers = scan_whitepapers()
        
        summary = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "recent_commits": git_logs,
            "documented_files": whitepapers
        }
        
        output_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        output_path = os.path.join(output_dir, 'TOAI_Generated', 'release_summary.json')
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
            
        print(f"Release summary successfully written to {output_path}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
