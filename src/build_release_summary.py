# -*- coding: utf-8 -*-
import sys
import os
import subprocess
import datetime
import json

def get_git_log(max_count=20):
    try:
        cmd = ['git', 'log', f'-n', str(max_count), '--pretty=format:%h - %an, %ar : %s']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True, cwd=os.getcwd())
        return result.stdout.splitlines()
    except Exception as e:
        print(f"Warning: Failed to fetch git log: {e}")
        return []

def scan_whitepapers():
    whitepapers = []
    docs_dir = os.path.join(os.getcwd(), 'docs')
    if os.path.exists(docs_dir):
        for root, dirs, files in os.walk(docs_dir):
            for file in files:
                if file.endswith('.md') or file.endswith('.txt'):
                    whitepapers.append(os.path.join(root, file))
    return whitepapers

def main():
    print("=== TOAI Release Summary Builder ===")
    logs = get_git_log(15)
    whitepapers = scan_whitepapers()
    
    summary_data = {
        "timestamp": datetime.datetime.now().isoformat(),
        "recent_commits": logs,
        "whitepapers_found": whitepapers
    }
    
    output_path = os.path.join(os.getcwd(), 'release_summary.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, ensure_ascii=False, indent=2)
        
    print(f"Successfully generated release summary at: {output_path}")

if __name__ == '__main__':
    main()
