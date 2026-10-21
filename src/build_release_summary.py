import sys
import os
import subprocess
import datetime
import json

def get_git_log():
    try:
        result = subprocess.run(
            ['git', 'log', '-n', '10', '--pretty=format:%h - %an, %ar : %s'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Git log unavailable: {str(e)}"]

def scan_whitepaper():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    potential_paths = [
        os.path.join(workspace, 'WHITE_PAPER.md'),
        os.path.join(workspace, 'README.md')
    ]
    summary = []
    for path in potential_paths:
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    summary.append(f"--- File: {os.path.basename(path)} ---")
                    summary.extend([line.strip() for line in lines[:15] if line.strip()])
            except Exception as e:
                summary.append(f"Error reading {path}: {str(e)}")
    if not summary:
        summary.append("No whitepaper or README found.")
    return summary

def main():
    print("Building release summary...")
    git_commits = get_git_log()
    whitepaper_summary = scan_whitepaper()
    
    release_info = {
        "timestamp": datetime.datetime.now().isoformat(),
        "recent_commits": git_commits,
        "whitepaper_summary": whitepaper_summary
    }
    
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    out_dir = os.path.join(workspace, 'TOAI_Generated')
    os.makedirs(out_dir, exist_ok=True)
    
    out_path = os.path.join(out_dir, 'release_summary.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(release_info, f, ensure_ascii=False, indent=2)
        
    print(f"Release summary successfully generated at: {out_path}")

if __name__ == '__main__':
    main()
