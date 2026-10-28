import sys
import os
import traceback
import subprocess
import datetime
import json

def get_git_logs():
    try:
        result = subprocess.run(
            ['git', 'log', '-n', '10', '--pretty=format:%h - %an, %ar : %s'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Git log retrieval failed: {str(e)}"]

def scan_whitepaper():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    whitepaper_path = os.path.join(workspace_dir, 'WHITEPAPER.md')
    if os.path.exists(whitepaper_path):
        try:
            with open(whitepaper_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.splitlines()
                return lines[:15]
        except Exception as e:
            return [f"Error reading whitepaper: {str(e)}"]
    return ["Whitepaper not found."]

def main():
    try:
        print("Starting release summary build process...")
        logs = get_git_logs()
        whitepaper_summary = scan_whitepaper()
        
        summary_data = {
            "timestamp": datetime.datetime.now().isoformat(),
            "git_recent_commits": logs,
            "whitepaper_excerpt": whitepaper_summary
        }
        
        workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
        os.makedirs(output_dir, exist_ok=True)
        
        output_path = os.path.join(output_dir, 'release_summary.json')
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, ensure_ascii=False, indent=2)
            
        print(f"Release summary successfully generated at: {output_path}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
