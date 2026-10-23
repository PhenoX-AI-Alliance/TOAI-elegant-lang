import sys
import os
import subprocess
import json
from datetime import datetime

def get_git_log(max_count=10):
    try:
        cmd = ['git', 'log', f'-n', str(max_count), '--pretty=format:%h - %an, %ar : %s']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True, encoding='utf-8')
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Git log retrieval failed: {str(e)}"]

def scan_whitepaper():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    possible_paths = [
        os.path.join(workspace_dir, 'TOAI-elegant-lang', 'WHITEPAPER.md'),
        os.path.join(workspace_dir, 'WHITEPAPER.md')
    ]
    for path in possible_paths:
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    return ''.join(lines[:30])
            except Exception as e:
                return f"Error reading whitepaper: {str(e)}"
    return "Whitepaper not found."

def main():
    print("Generating release summary...")
    logs = get_git_log()
    whitepaper_snippet = scan_whitepaper()
    
    summary = {
        "timestamp": datetime.now().isoformat(),
        "git_logs": logs,
        "whitepaper_overview": whitepaper_snippet
    }
    
    output_dir = os.path.join(os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/'), 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'release_summary.json')
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
        
    print(f"Release summary successfully written to {output_path}")

if __name__ == '__main__':
    main()