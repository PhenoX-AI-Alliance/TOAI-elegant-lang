import sys
import os
import subprocess
import datetime
import json

def get_git_log(max_count=10):
    try:
        result = subprocess.run(
            ['git', 'log', f'-n', str(max_count), '--pretty=format:%h - %an, %ar : %s'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Git log unavailable: {str(e)}"]

def scan_whitepapers():
    docs = []
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    search_paths = [
        os.path.join(workspace, 'TOAI-elegant-lang'),
        workspace
    ]
    for path in search_paths:
        if os.path.exists(path):
            for root, dirs, files in os.walk(path):
                for file in files:
                    if 'whitepaper' in file.lower() or file.endswith('.md'):
                        docs.append(os.path.join(root, file))
    return docs

def main():
    print("=== TOAI Release Summary Builder ===")
    logs = get_git_log(15)
    whitepapers = scan_whitepapers()
    
    summary = {
        "timestamp": datetime.datetime.now().isoformat(),
        "recent_commits": logs,
        "related_documents": whitepapers[:10]
    }
    
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    out_path = os.path.join(workspace, 'TOAI_Generated', 'release_summary.json')
    
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
        
    print(f"Release summary successfully generated at: {out_path}")

if __name__ == '__main__':
    main()
