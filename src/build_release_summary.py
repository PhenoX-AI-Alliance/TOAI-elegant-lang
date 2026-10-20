import sys
import os
import traceback
import subprocess
import json
from datetime import datetime

def get_git_log(max_count=20):
    try:
        cmd = ['git', 'log', f'-n', str(max_count), '--pretty=format:%h - %an, %ar : %s']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=10)
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Error fetching git log: {str(e)}"]

def scan_whitepaper():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    possible_paths = [
        os.path.join(workspace_dir, 'WHITEPAPER.md'),
        os.path.join(workspace_dir, 'docs', 'WHITEPAPER.md'),
        os.path.join(workspace_dir, 'TOAI-elegant-lang', 'WHITEPAPER.md')
    ]
    for path in possible_paths:
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    return path, content[:1000] # Return path and first 1000 chars as summary
            except Exception:
                pass
    return None, "Whitepaper not found."

def main():
    try:
        print("Starting Release Summary Generation...")
        git_history = get_git_log()
        wp_path, wp_summary = scan_whitepaper()
        
        summary_data = {
            "timestamp": datetime.now().isoformat(),
            "git_recent_commits": git_history,
            "whitepaper_source": wp_path,
            "whitepaper_excerpt": wp_summary
        }
        
        workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        output_json_path = os.path.join(workspace_dir, 'TOAI_Generated', 'release_summary.json')
        
        with open(output_json_path, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, ensure_ascii=False, indent=2)
            
        print(f"Release summary successfully generated at: {output_json_path}")
    except Exception as e:
        print(f"Error in build_release_summary: {e}", file=sys.stderr)
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
