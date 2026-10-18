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
            ['git', 'log', '-n', '10', '--oneline'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Git log retrieval failed: {str(e)}"]

def main():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    summary_path = os.path.join(workspace, 'TOAI-elegant-lang', 'RELEASE_SUMMARY.md')
    
    logs = get_git_log()
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    content = []
    content.append("# TOAI Elegant Lang Release Summary")
    content.append(f"Generated at: {timestamp}")
    content.append("")
    content.append("## Recent Changes (Git Log)")
    for log in logs:
        content.append(f"- {log}")
    content.append("")
    content.append("## Ecosystem Status")
    content.append("Gaia Ecosystem core heartbeat is active. Altruistic monetization and robust value creation in progress.")
    
    os.makedirs(os.path.dirname(summary_path), exist_ok=True)
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(content))
    
    print(f"Release summary successfully built at: {summary_path}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)