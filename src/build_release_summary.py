# -*- coding: utf-8 -*-
import sys
import os
import traceback
import time
import json
import subprocess
import datetime

def get_git_log():
    try:
        result = subprocess.run(
            ['git', 'log', '-n', '10', '--pretty=format:%h - %an: %s (%ar)'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Git log retrieval failed: {str(e)}"]

def scan_whitepaper(workspace_dir):
    whitepaper_path = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'docs', 'whitepaper.md')
    if os.path.exists(whitepaper_path):
        try:
            with open(whitepaper_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            return ''.join(lines[:20]) # return first 20 lines as summary
        except Exception as e:
            return f"Failed to read whitepaper: {str(e)}"
    return "Whitepaper not found."

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = os.path.join(output_dir, 'release_summary.json')
    
    git_logs = get_git_log()
    whitepaper_summary = scan_whitepaper(workspace_dir)
    
    release_data = {
        "timestamp": datetime.datetime.now().isoformat(),
        "version": "1.0.0-gaia",
        "git_recent_commits": git_logs,
        "whitepaper_summary": whitepaper_summary,
        "message": "Gaia Ecosystem Release Summary generated successfully with altruistic intent."
    }
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(release_data, f, ensure_ascii=False, indent=4)
        print(f"Successfully generated release summary at: {output_file}")
    except Exception as e:
        print(f"Error writing release summary file: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
