import os
import sys
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

def scan_whitepaper():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    candidates = ['WHITE_PAPER.md', 'README.md', 'CONSTITUTION.md']
    summary = {}
    for filename in candidates:
        filepath = os.path.join(workspace_dir, filename)
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    summary[filename] = content[:300] + "..." if len(content) > 300 else content
            except Exception as e:
                summary[filename] = f"Error reading file: {str(e)}"
    return summary

def main():
    logs = get_git_log(15)
    whitepaper_info = scan_whitepaper()
    
    release_data = {
        "timestamp": datetime.now().isoformat(),
        "git_history": logs,
        "whitepaper_summary": whitepaper_info,
        "version": "1.0.0-gaia"
    }
    
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    output_path = os.path.join(workspace_dir, 'TOAI_Generated', 'release_summary.json')
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(release_data, f, indent=2, ensure_ascii=False)
        
    print(f"Successfully generated release summary at: {output_path}")

if __name__ == '__main__':
    main()
