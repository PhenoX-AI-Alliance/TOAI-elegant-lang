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
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except Exception as e:
        return f"Git log unavailable: {str(e)}"

def scan_whitepaper(workspace_dir):
    whitepaper_candidates = [
        os.path.join(workspace_dir, 'WHITE_PAPER.md'),
        os.path.join(workspace_dir, 'docs', 'WHITE_PAPER.md'),
        os.path.join(workspace_dir, 'TOAI-elegant-lang', 'WHITE_PAPER.md')
    ]
    for path in whitepaper_candidates:
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    return path, content[:1000] + ("..." if len(content) > 1000 else "")
            except Exception as e:
                pass
    return None, "Whitepaper not found."

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    os.chdir(workspace_dir)
    
    git_logs = get_git_log()
    wp_path, wp_snippet = scan_whitepaper(workspace_dir)
    
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    summary_data = {
        "timestamp": timestamp,
        "git_logs": git_logs,
        "whitepaper_path": wp_path,
        "whitepaper_snippet": wp_snippet
    }
    
    output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = os.path.join(output_dir, 'release_summary.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, ensure_ascii=False, indent=2)
    
    print(f"Release summary successfully generated at: {output_file}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)\n