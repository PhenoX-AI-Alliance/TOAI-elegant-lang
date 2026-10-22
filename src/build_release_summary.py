import sys
import os
import subprocess
import json
from datetime import datetime

def get_git_log(max_count=10):
    try:
        result = subprocess.run(
            ['git', 'log', f'-n {max_count}', '--pretty=format:%h - %an, %ar : %s'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Git log unavailable: {str(e)}"]

def scan_whitepaper(workspace):
    whitepaper_paths = [
        os.path.join(workspace, 'WHITEPAPER.md'),
        os.path.join(workspace, 'TOAI-elegant-lang', 'WHITEPAPER.md')
    ]
    for path in whitepaper_paths:
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    for line in lines:
                        if "version" in line.lower() or "release" in line.lower():
                            return line.strip()
            except Exception:
                pass
    return "Version info not found in whitepaper."

def main():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    os.chdir(workspace)
    
    print("Scanning repository and whitepaper for release summary...")
    version_info = scan_whitepaper(workspace)
    logs = get_git_log(15)
    
    summary = {
        "timestamp": datetime.now().isoformat(),
        "version_hint": version_info,
        "recent_commits": logs
    }
    
    output_path = os.path.join(workspace, 'TOAI_Generated', 'release_summary.json')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
        
    print(f"Release summary successfully generated at: {output_path}")

if __name__ == '__main__':
    main()
