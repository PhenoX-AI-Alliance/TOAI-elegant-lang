import sys
import os
import traceback
import time
import json
import subprocess
import datetime

def get_git_log():
    try:
        if not os.path.exists('.git'):
            return "No git repository found."
        result = subprocess.run(
            ['git', 'log', '-n', '10', '--oneline'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout
    except Exception as e:
        return f"Error fetching git log: {str(e)}"

def scan_whitepaper():
    whitepaper_paths = ['WHITE_PAPER.md', 'CONSTITUTION.md', 'README.md']
    summary = {}
    for path in whitepaper_paths:
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    summary[path] = content[:200] + "..." if len(content) > 200 else content
            except Exception as e:
                summary[path] = f"Error reading file: {str(e)}"
        else:
            summary[path] = "File not found."
    return summary

def main():
    print("Starting release summary generation...")
    git_log = get_git_log()
    whitepaper_info = scan_whitepaper()
    
    release_data = {
        "timestamp": datetime.datetime.now().isoformat(),
        "git_recent_commits": git_log,
        "whitepaper_summary": whitepaper_info
    }
    
    output_filename = "release_summary.json"
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    generated_dir = os.path.join(workspace, 'TOAI_Generated')
    os.makedirs(generated_dir, exist_ok=True)
    
    output_filepath = os.path.join(generated_dir, output_filename)
    
    with open(output_filepath, 'w', encoding='utf-8') as f:
        json.dump(release_data, f, ensure_ascii=False, indent=4)
        
    print(f"Release summary successfully generated at: {output_filepath}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
