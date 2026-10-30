import sys
import os
import traceback
import subprocess
import datetime
import json

def get_git_log():
    try:
        cmd = ['git', 'log', '-n', '10', '--oneline']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip().split('\n')
    except Exception as e:
        return [f"Git log unavailable: {str(e)}"]

def scan_whitepapers():
    docs = []
    base_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    target = os.path.join(base_dir, 'TOAI-elegant-lang')
    if os.path.exists(target):
        for root, dirs, files in os.walk(target):
            for file in files:
                if file.endswith('.md') or file.endswith('.txt'):
                    docs.append(os.path.join(root, file))
    return docs

def main():
    print("Building release summary...")
    logs = get_git_log()
    papers = scan_whitepapers()
    
    summary = {
        "timestamp": datetime.datetime.now().isoformat(),
        "recent_commits": logs,
        "available_documents": papers
    }
    
    base_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    out_dir = os.path.join(base_dir, 'TOAI_Generated')
    os.makedirs(out_dir, exist_ok=True)
    
    out_path = os.path.join(out_dir, 'release_summary.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
        
    print(f"Release summary successfully generated at: {out_path}")

if __name__ == '__main__':
    main()
