import sys
import os
import subprocess
import datetime
import json

def get_git_log(max_count=10):
    try:
        cmd = ['git', 'log', f'-n', str(max_count), '--pretty=format:%h - %an, %ar : %s']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=10)
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Git log unavailable: {str(e)}"]

def scan_whitepapers():
    papers = []
    try:
        for root, dirs, files in os.walk('.'):
            for file in files:
                if 'whitepaper' in file.lower() or 'doc' in file.lower() or file.endswith('.md'):
                    papers.append(os.path.join(root, file))
    except Exception as e:
        pass
    return papers[:5]

def generate_release_summary():
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    logs = get_git_log()
    papers = scan_whitepapers()
    
    summary = {
        "timestamp": timestamp,
        "git_recent_commits": logs,
        "related_documents": papers,
        "status": "release_summary_ready"
    }
    
    output_file = "release_summary.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    print(f"Successfully generated {output_file} at {timestamp}")

if __name__ == '__main__':
    generate_release_summary()
