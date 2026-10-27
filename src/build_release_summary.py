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

def scan_whitepaper(workspace_dir):
    whitepaper_path = os.path.join(workspace_dir, 'TOAI_Generated', 'whitepaper.md')
    if os.path.exists(whitepaper_path):
        try:
            with open(whitepaper_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return content[:500] + "..." if len(content) > 500 else content
        except Exception as e:
            return f"Error reading whitepaper: {str(e)}"
    return "No whitepaper found."

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    print("=== TOAI Release Summary Generator ===")
    print(f"Timestamp: {datetime.datetime.now().isoformat()}")
    
    logs = get_git_log()
    whitepaper_summary = scan_whitepaper(workspace_dir)
    
    summary_data = {
        "timestamp": datetime.datetime.now().isoformat(),
        "git_logs": logs,
        "whitepaper_excerpt": whitepaper_summary
    }
    
    out_path = os.path.join(workspace_dir, 'TOAI_Generated', 'release_summary.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, ensure_ascii=False, indent=2)
    
    print(f"Release summary successfully generated at: {out_path}")

if __name__ == '__main__':
    main()
