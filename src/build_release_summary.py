import sys
import os
import subprocess
import json
import datetime

def get_git_log(max_count=10):
    repo_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    if not os.path.exists(os.path.join(repo_dir, '.git')):
        return "Git repository not found."
    try:
        cmd = ['git', '-C', repo_dir, 'log', f'-n {max_count}', '--pretty=format:%h - %an, %ar : %s']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout
    except Exception as e:
        return f"Error fetching git log: {str(e)}"

def scan_whitepaper():
    repo_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    whitepaper_candidates = [
        os.path.join(repo_dir, 'WHITE_PAPER.md'),
        os.path.join(repo_dir, 'docs', 'WHITE_PAPER.md'),
        os.path.join(repo_dir, 'README.md')
    ]
    for path in whitepaper_candidates:
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read(500)
                    return f"Found document: {path}\nPreview:\n{content}..."
            except Exception as e:
                continue
    return "No whitepaper or main readme found."

def main():
    print("=== TOAI Release Summary Generator ===")
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    git_log = get_git_log(15)
    whitepaper_info = scan_whitepaper()
    
    summary = {
        "timestamp": timestamp,
        "git_log": git_log,
        "whitepaper_summary": whitepaper_info
    }
    
    output_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'TOAI_Generated', 'release_summary.json'))
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
        
    print(f"Release summary successfully generated at: {output_path}")

if __name__ == '__main__':
    main()
