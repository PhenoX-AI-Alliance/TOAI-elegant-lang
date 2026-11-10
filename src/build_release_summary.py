import sys
import os
import subprocess
import json
import datetime

def get_git_log():
    try:
        result = subprocess.run(
            ['git', 'log', '-n', '10', '--pretty=format:%h - %an, %ar : %s'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Git log error: {str(e)}"]

def main():
    print("Generating Release Summary...")
    logs = get_git_log()
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    summary = {
        "timestamp": timestamp,
        "recent_commits": logs,
        "version": "1.0.0",
        "status": "release_ready"
    }
    
    base_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    output_path = os.path.join(base_dir, 'TOAI_Generated', 'release_summary.json')
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
        
    print(f"Release summary successfully written to {output_path}")

if __name__ == '__main__':
    main()
