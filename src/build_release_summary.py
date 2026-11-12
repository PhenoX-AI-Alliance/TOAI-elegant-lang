import sys
import os
import traceback
import time
import json
import subprocess
from datetime import datetime

def get_git_log():
    try:
        result = subprocess.run(
            ['git', 'log', '-n', '10', '--oneline'],
            capture_output=True,
            text=True,
            check=True,
            cwd=os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        )
        return result.stdout.strip().split('\n')
    except Exception as e:
        return [f"Git log retrieval failed: {str(e)}"]

def scan_whitepaper():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    wp_path = os.path.join(workspace, 'TOAI-elegant-lang', 'WHITE_PAPER.md')
    if os.path.exists(wp_path):
        try:
            with open(wp_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.splitlines()
                return lines[:20]
        except Exception as e:
            return [f"Failed to read whitepaper: {str(e)}"]
    return ["Whitepaper not found."]

def main():
    try:
        workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        output_dir = os.path.join(workspace, 'TOAI_Generated')
        os.makedirs(output_dir, exist_ok=True)
        
        logs = get_git_log()
        whitepaper_snippet = scan_whitepaper()
        
        summary = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "version": "1.0.0",
            "recent_commits": logs,
            "whitepaper_overview": whitepaper_snippet
        }
        
        out_file = os.path.join(output_dir, 'release_summary.json')
        with open(out_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
            
        print(f"Release summary successfully generated at: {out_file}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
