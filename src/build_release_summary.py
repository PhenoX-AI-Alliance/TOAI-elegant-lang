import sys
import os
import subprocess
import json
from datetime import datetime

def get_git_log():
    try:
        cmd = ['git', 'log', '-n', '10', '--pretty=format:%h - %an, %ar : %s']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True, cwd=os.path.dirname(os.path.abspath(__file__)))
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Git log retrieval failed: {str(e)}"]

def scan_whitepaper():
    wp_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'WHITEPAPER.md')
    if os.path.exists(wp_path):
        try:
            with open(wp_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            return [line.strip() for line in lines[:20] if line.strip()]
        except Exception as e:
            return [f"Error reading whitepaper: {str(e)}"]
    return ["Whitepaper not found."]

def main():
    print("Generating release summary...")
    logs = get_git_log()
    wp_summary = scan_whitepaper()
    
    report = {
        "timestamp": datetime.now().isoformat(),
        "recent_commits": logs,
        "whitepaper_excerpt": wp_summary
    }
    
    output_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'release_summary.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
        
    print(f"Release summary successfully written to {output_file}")

if __name__ == '__main__':
    main()
