import sys
import os
import traceback
import subprocess
import json
from datetime import datetime

def get_git_log():
    try:
        result = subprocess.run(
            ['git', 'log', '-n', '10', '--pretty=format:%h - %an, %ar: %s'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Git log retrieval failed: {str(e)}"]

def scan_whitepaper(base_dir):
    wp_path = os.path.join(base_dir, 'TOAI_Generated', 'whitepaper.md')
    if os.path.exists(wp_path):
        try:
            with open(wp_path, 'r', encoding='utf-8') as f:
                return f.read()[:500] + "... [truncated]"
        except Exception as e:
            return f"Failed to read whitepaper: {str(e)}"
    return "Whitepaper not found."

def main():
    try:
        base_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        logs = get_git_log()
        whitepaper_summary = scan_whitepaper(base_dir)
        
        release_data = {
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0",
            "recent_commits": logs,
            "whitepaper_excerpt": whitepaper_summary
        }
        
        out_path = os.path.join(base_dir, 'TOAI_Generated', 'release_summary.json')
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(release_data, f, ensure_ascii=False, indent=2)
            
        print(f"Successfully generated release summary at {out_path}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
