import sys
import os
import subprocess
import json
from datetime import datetime

def get_git_log(max_count=20):
    repo_path = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    git_dir = os.path.join(repo_path, '.git')
    if not os.path.exists(git_dir):
        return "Git repository not initialized or found."
    try:
        cmd = ['git', '-C', repo_path, 'log', f'-n {max_count}', '--pretty=format:%h - %an, %ar : %s']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout
    except Exception as e:
        return f"Error fetching git log: {str(e)}"

def scan_whitepaper():
    repo_path = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    possible_paths = [
        os.path.join(repo_path, 'WHITEPAPER.md'),
        os.path.join(repo_path, 'CONSTITUTION.md'),
        os.path.join(repo_path, 'TOAI-elegant-lang', 'WHITEPAPER.md')
    ]
    found_info = []
    for p in possible_paths:
        if os.path.exists(p):
            try:
                with open(p, 'r', encoding='utf-8') as f:
                    content = f.read(200)
                    found_info.append(f"File: {os.path.basename(p)}, Preview: {content.strip()[:100]}...")
            except Exception as e:
                found_info.append(f"File: {os.path.basename(p)}, Error reading: {str(e)}")
    return found_info if found_info else ["No whitepaper found."]

def main():
    print("Generating release summary...")
    git_logs = get_git_log()
    whitepaper_info = scan_whitepaper()
    
    summary = {
        "timestamp": datetime.now().isoformat(),
        "git_history": git_logs,
        "whitepaper_scans": whitepaper_info,
        "status": "success"
    }
    
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = os.path.join(output_dir, 'release_summary.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
        
    print(f"Release summary successfully generated at: {output_file}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"Error in release summary builder: {e}", file=sys.stderr)
        sys.exit(1)
