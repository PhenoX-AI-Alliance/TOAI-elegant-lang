import os
import sys
import subprocess
import json
import datetime
import traceback

def get_git_logs(max_count=20):
    try:
        cmd = ['git', 'log', f'-n {max_count}', '--pretty=format:%h - %an: %s (%ad)', '--date=short']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.splitlines()
    except Exception as e:
        print(f"Warning: Could not fetch git logs: {e}")
        return []

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
                    if file.endswith('.md') and ('whitepaper' in file.lower() or 'release' in file.lower() or 'doc' in file.lower()):
                        docs.append(os.path.join(root, file))
    return docs

def main():
    try:
        print("Starting release summary generation...")
        logs = get_git_logs(30)
        papers = scan_whitepapers()
        
        summary = {
            "generated_at": datetime.datetime.now().isoformat(),
            "git_logs_count": len(logs),
            "recent_commits": logs[:10],
            "related_documents": papers[:10]
        }
        
        workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        out_dir = os.path.join(workspace, 'TOAI_Generated')
        os.makedirs(out_dir, exist_ok=True)
        
        out_path = os.path.join(out_dir, 'release_summary.json')
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
            
        print(f"Release summary successfully written to {out_path}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
