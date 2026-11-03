import sys
import os
import traceback
import subprocess
import json
from datetime import datetime

def get_git_log(repo_path, max_count=20):
    try:
        if not os.path.exists(os.path.join(repo_path, '.git')):
            return "Git repository not initialized."
        cmd = ['git', '-C', repo_path, 'log', f'-n', str(max_count), '--pretty=format:%h - %an, %ar : %s']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout
    except Exception as e:
        return f"Error fetching git log: {str(e)}"

def scan_whitepaper(workspace_path):
    whitepaper_candidates = [
        os.path.join(workspace_path, 'WHITEPAPER.md'),
        os.path.join(workspace_path, 'TOAI-elegant-lang', 'WHITEPAPER.md'),
        os.path.join(workspace_path, 'CONSTITUTION.md')
    ]
    found_info = {}
    for path in whitepaper_candidates:
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    found_info[path] = content[:500] + ('...' if len(content) > 500 else '')
            except Exception as e:
                found_info[path] = f"Error reading file: {str(e)}"
    return found_info

def main():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_path = os.path.join(workspace, 'TOAI-elegant-lang')
    
    print("=== TOAI Release Summary Builder ===")
    print(f"Target Repository: {repo_path}")
    
    git_logs = get_git_log(repo_path)
    whitepaper_data = scan_whitepaper(workspace)
    
    summary = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "git_recent_commits": git_logs,
        "whitepaper_snippets": whitepaper_data
    }
    
    output_dir = os.path.join(workspace, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, 'release_summary.json')
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=4)
        print(f"Successfully generated release summary at: {output_file}")
    except Exception as e:
        print(f"Failed to write release summary: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)\n