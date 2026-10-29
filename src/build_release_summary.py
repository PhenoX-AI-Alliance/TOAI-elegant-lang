#!/usr/bin/env python3
import sys
import os
import subprocess
import json
import datetime

def get_git_log():
    try:
        cmd = ["git", "log", "-n", "10", "--oneline"]
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return res.stdout.strip().splitlines()
    except Exception as e:
        return [f"Git log unavailable: {e}"]

def scan_whitepaper(workspace):
    papers = []
    try:
        for root, dirs, files in os.walk(workspace):
            for file in files:
                if "whitepaper" in file.lower() or file.endswith(".md"):
                    papers.append(os.path.join(root, file))
    except Exception as e:
        pass
    return papers[:5]

def main():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    logs = get_git_log()
    papers = scan_whitepaper(workspace)
    
    summary = {
        "timestamp": datetime.datetime.now().isoformat(),
        "recent_commits": logs,
        "related_documents": papers,
        "version": "1.0.0-gaia"
    }
    
    output_dir = os.path.join(workspace, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    out_file = os.path.join(output_dir, 'release_summary.json')
    
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
        
    print(f"Release summary successfully generated at: {out_file}")

if __name__ == '__main__':
    main()
