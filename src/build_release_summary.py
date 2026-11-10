import sys
import os
import traceback
import subprocess
import json
from datetime import datetime

def get_git_log(repo_path, max_count=20):
    try:
        cmd = ['git', '-C', repo_path, 'log', f'-n', str(max_count), '--pretty=format:%h - %an, %ar : %s']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Error fetching git log: {str(e)}"]

def scan_whitepaper(repo_path):
    whitepaper_path = os.path.join(repo_path, 'WHITEPAPER.md')
    if os.path.exists(whitepaper_path):
        try:
            with open(whitepaper_path, 'r', encoding='utf-8') as f:
                content = f.read()
                return content[:500] + "..." if len(content) > 500 else content
        except Exception as e:
            return f"Error reading WHITEPAPER.md: {str(e)}"
    return "WHITEPAPER.md not found."

def main():
    try:
        workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        repo_path = os.path.join(workspace_dir, 'TOAI-elegant-lang')
        
        if not os.path.exists(repo_path):
            print(f"Repository path does not exist: {repo_path}")
            sys.exit(1)
            
        print("Scanning Git log...")
        git_logs = get_git_log(repo_path)
        
        print("Scanning Whitepaper...")
        whitepaper_summary = scan_whitepaper(repo_path)
        
        release_data = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "git_logs": git_logs,
            "whitepaper_summary": whitepaper_summary
        }
        
        output_path = os.path.join(repo_path, 'release_summary.json')
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(release_data, f, ensure_ascii=False, indent=2)
            
        print(f"Release summary successfully built at: {output_path}")
        
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
