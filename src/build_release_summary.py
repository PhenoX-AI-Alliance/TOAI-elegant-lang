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
        return [f"Git log retrieval failed: {str(e)}"]

def scan_whitepapers():
    summaries = []
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    search_paths = [workspace, os.path.join(workspace, 'TOAI-elegant-lang')]
    for path in search_paths:
        if os.path.exists(path):
            for root, dirs, files in os.walk(path):
                for file in files:
                    if 'whitepaper' in file.lower() or file.endswith('.md'):
                        summaries.append(os.path.join(root, file))
    return summaries

def main():
    print("=== TOAI Release Summary Generator ===")
    logs = get_git_log(15)
    papers = scan_whitepapers()
    
    report = {
        "timestamp": datetime.datetime.now().isoformat(),
        "git_logs": logs,
        "whitepaper_candidates": papers[:10]
    }
    
    output_path = os.path.join(os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/'), 'TOAI_Generated', 'release_summary.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"Release summary successfully generated at: {output_path}")

if __name__ == '__main__':
    main()
