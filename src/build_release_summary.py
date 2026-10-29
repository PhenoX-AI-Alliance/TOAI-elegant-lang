import sys
import os
import subprocess
import json
import datetime

def get_git_log():
    try:
        result = subprocess.run(
            ['git', 'log', '-n', '10', '--pretty=format:%h - %an: %s (%ad)'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Git log unavailable: {str(e)}"]

def scan_whitepapers():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    papers = []
    try:
        for root, dirs, files in os.walk(workspace):
            for file in files:
                if 'whitepaper' in file.lower() or file.endswith('.md'):
                    papers.append(os.path.join(root, file))
    except Exception as e:
        pass
    return papers

def main():
    print("Generating release summary...")
    logs = get_git_log()
    papers = scan_whitepapers()
    
    summary = {
        "timestamp": datetime.datetime.now().isoformat(),
        "recent_commits": logs,
        "whitepapers_found": papers[:5]
    }
    
    output_path = os.path.join(os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/'), 'TOAI_Generated', 'release_summary.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    print(f"Release summary successfully written to {output_path}")

if __name__ == '__main__':
    main()
