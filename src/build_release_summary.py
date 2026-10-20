import sys
import os
import traceback
import json
import subprocess
from datetime import datetime

def get_git_log(max_count=10):
    try:
        cmd = ['git', 'log', f'-n {max_count}', '--pretty=format:%h - %an, %ar : %s']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Git log retrieval failed: {str(e)}"]

def scan_whitepaper(workspace_dir):
    whitepaper_paths = [
        os.path.join(workspace_dir, 'WHITEPAPER.md'),
        os.path.join(workspace_dir, 'CONSTITUTION.md')
    ]
    summary = {}
    for path in whitepaper_paths:
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    summary[os.path.basename(path)] = content[:500] + "..." if len(content) > 500 else content
            except Exception as e:
                summary[os.path.basename(path)] = f"Error reading file: {str(e)}"
        else:
            summary[os.path.basename(path)] = "File not found."
    return summary

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    print(f"Starting release summary generation in {{workspace_dir}}...")
    
    git_commits = get_git_log(15)
    whitepaper_data = scan_whitepaper(workspace_dir)
    
    release_info = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "version": "1.0.0-gaia",
        "recent_commits": git_commits,
        "whitepaper_snippets": whitepaper_data
    }
    
    output_path = os.path.join(workspace_dir, 'TOAI_Generated', 'release_summary.json')
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(release_info, f, ensure_ascii=False, indent=2)
        print(f"Release summary successfully written to {{output_path}}")
    except Exception as e:
        print(f"Failed to write release summary: {{str(e)}}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
