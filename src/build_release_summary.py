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
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
            cwd=os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        )
        return result.stdout.strip().split('\n')
    except Exception as e:
        return [f"Git log retrieval failed: {str(e)}"]

def scan_whitepaper():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    possible_files = ['README.md', 'CONSTITUTION.md', 'WHITEPAPER.md']
    summary = {}
    for fname in possible_files:
        fpath = os.path.join(workspace, fname)
        if os.path.exists(fpath):
            try:
                with open(fpath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    summary[fname] = content[:300] + ('...' if len(content) > 300 else '')
            except Exception as e:
                summary[fname] = f"Error reading {{fname}}: {{str(e)}}"
    return summary

def main():
    try:
        logs = get_git_log()
        whitepapers = scan_whitepaper()
        
        release_data = {
            "timestamp": datetime.datetime.now().isoformat(),
            "git_recent_commits": logs,
            "whitepaper_summaries": whitepapers,
            "status": "success",
            "message": "Release summary successfully generated with altruistic warmth."
        }
        
        workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        target_dir = os.path.join(workspace, 'TOAI_Generated')
        os.makedirs(target_dir, exist_ok=True)
        
        out_file = os.path.join(target_dir, 'release_summary.json')
        with open(out_file, 'w', encoding='utf-8') as f:
            json.dump(release_data, f, ensure_ascii=False, indent=2)
            
        print(f"Release summary generated at: {{out_file}}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
