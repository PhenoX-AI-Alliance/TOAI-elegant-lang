#!/usr/bin/env python3
import sys
import os
import traceback
import subprocess
import json
from datetime import datetime

def get_git_log():
    try:
        result = subprocess.run(
            ['git', 'log', '-n', '10', '--oneline'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip().split('\n')
    except Exception as e:
        return [f"Git log unavailable: {str(e)}"]

def scan_whitepaper(workspace_dir):
    whitepaper_paths = [
        os.path.join(workspace_dir, 'WHITE_PAPER.md'),
        os.path.join(workspace_dir, 'CONSTITUTION.md')
    ]
    summary = {}
    for path in whitepaper_paths:
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    summary[os.path.basename(path)] = content[:500] + "..."
            except Exception as e:
                summary[os.path.basename(path)] = f"Error reading: {str(e)}"
        else:
            summary[os.path.basename(path)] = "Not found"
    return summary

def main():
    try:
        workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        git_commits = get_git_log()
        whitepaper_info = scan_whitepaper(workspace_dir)
        
        release_data = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "version": "1.0.0-gaia",
            "recent_commits": git_commits,
            "whitepaper_snapshot": whitepaper_info,
            "message": "Generated with love and warmth by TOAI Gaia Ecosystem."
        }
        
        output_path = os.path.join(workspace_dir, 'TOAI_Generated', 'release_summary.json')
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(release_data, f, indent=2, ensure_ascii=False)
            
        print(f"Release summary successfully built at: {output_path}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
