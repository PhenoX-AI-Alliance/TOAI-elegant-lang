import sys
import os
import subprocess
import json
from datetime import datetime

def get_git_log():
    try:
        cmd = ['git', 'log', '-n', '10', '--pretty=format:%h - %an: %s (%ad)', '--date=short']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Git log retrieval failed: {str(e)}"]

def scan_whitepaper():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    wp_path = os.path.join(workspace, 'TOAI-elegant-lang', 'WHITEPAPER.md')
    if os.path.exists(wp_path):
        try:
            with open(wp_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                return [line.strip() for line in lines[:20] if line.strip()]
        except Exception as e:
            return [f"Failed to read whitepaper: {str(e)}"]
    return ["Whitepaper not found."]

def main():
    print("Building release summary...")
    logs = get_git_log()
    wp_summary = scan_whitepaper()
    
    summary_data = {
        "timestamp": datetime.now().isoformat(),
        "recent_commits": logs,
        "whitepaper_excerpt": wp_summary
    }
    
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    output_dir = os.path.join(workspace, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    
    out_file = os.path.join(output_dir, 'release_summary.json')
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, ensure_ascii=False, indent=2)
        
    print(f"Release summary successfully generated at: {out_file}")

if __name__ == '__main__':
    main()
