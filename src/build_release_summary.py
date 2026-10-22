import sys
import os
import subprocess
import json
import datetime

def get_git_log(max_count=10):
    try:
        cmd = ['git', 'log', f'-n', str(max_count), '--pretty=format:%h - %an, %ar : %s']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Git log unavailable: {str(e)}"]

def scan_whitepaper():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    whitepaper_paths = [
        os.path.join(workspace, 'WHITE_PAPER.md'),
        os.path.join(workspace, 'CONSTITUTION.md')
    ]
    summary = {}
    for path in whitepaper_paths:
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    title = lines[0].strip() if lines else 'No Title'
                    summary[os.path.basename(path)] = {'title': title, 'lines': len(lines)}
            except Exception as e:
                summary[os.path.basename(path)] = {'error': str(e)}
    return summary

def main():
    print("=== TOAI Release Summary Builder ===")
    logs = get_git_log(15)
    whitepapers = scan_whitepaper()
    
    release_info = {
        'timestamp': datetime.datetime.now().isoformat(),
        'git_commits': logs,
        'whitepapers': whitepapers
    }
    
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    out_file = os.path.join(workspace, 'TOAI_Generated', 'release_summary.json')
    
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(release_info, f, ensure_ascii=False, indent=2)
        
    print(f"Release summary successfully generated at: {out_file}")

if __name__ == '__main__':
    main()
