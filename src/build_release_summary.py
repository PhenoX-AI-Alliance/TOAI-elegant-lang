import sys
import os
import subprocess
import datetime
import json

def get_git_log(max_count=10):
    try:
        cmd = ['git', 'log', f'-n', str(max_count), '--pretty=format:%h - %an, %ar : %s']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Git log unavailable: {str(e)}"]

def scan_whitepaper():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    candidates = [
        os.path.join(workspace, 'WHITE_PAPER.md'),
        os.path.join(workspace, 'CONSTITUTION.md'),
        os.path.join(workspace, 'README.md')
    ]
    summary = {}
    for path in candidates:
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    summary[os.path.basename(path)] = "".join(lines[:10])
            except Exception as e:
                summary[os.path.basename(path)] = f"Error reading: {str(e)}"
    return summary

def main():
    print("Building Release Summary...")
    logs = get_git_log(15)
    whitepapers = scan_whitepaper()
    
    release_data = {
        "timestamp": datetime.datetime.now().isoformat(),
        "git_logs": logs,
        "whitepaper_snippets": whitepapers
    }
    
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    out_file = os.path.join(workspace, 'TOAI_Generated', 'release_summary.json')
    
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(release_data, f, ensure_ascii=False, indent=2)
    
    print(f"Release summary successfully generated at: {out_file}")

if __name__ == '__main__':
    main()
