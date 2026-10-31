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
        print(f"Warning: Failed to fetch git log: {{e}}")
        return []

def scan_whitepaper():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    whitepaper_candidates = [
        os.path.join(workspace_dir, 'WHITEPAPER.md'),
        os.path.join(workspace_dir, 'docs', 'WHITEPAPER.md')
    ]
    for path in whitepaper_candidates:
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    return content[:500] + "..." if len(content) > 500 else content
            except Exception as e:
                print(f"Warning: Failed to read whitepaper at {{path}}: {{e}}")
    return "No whitepaper found."

def main():
    try:
        print("Starting release summary generation...")
        git_logs = get_git_log()
        whitepaper_summary = scan_whitepaper()
        
        summary_data = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "git_recent_commits": git_logs,
            "whitepaper_excerpt": whitepaper_summary
        }
        
        workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
        os.makedirs(output_dir, exist_ok=True)
        
        output_path = os.path.join(output_dir, 'release_summary.json')
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, indent=2, ensure_ascii=False)
            
        print(f"Release summary successfully written to {{output_path}}")
    except Exception as e:
        print(f"Error in release summary build: {{e}}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
