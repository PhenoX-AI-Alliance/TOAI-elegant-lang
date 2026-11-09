import sys
import os
import traceback
import subprocess
import json
import datetime

def get_git_log(repo_path, max_count=20):
    try:
        cmd = ['git', '-C', repo_path, 'log', f'-n', str(max_count), '--pretty=format:%h - %an: %s (%ad)']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Git log retrieval failed: {str(e)}"]

def scan_whitepaper(repo_path):
    wp_path = os.path.join(repo_path, 'WHITEPAPER.md')
    if os.path.exists(wp_path):
        try:
            with open(wp_path, 'r', encoding='utf-8') as f:
                return f.read()[:2000]
        except Exception as e:
            return f"Error reading WHITEPAPER.md: {str(e)}"
    return "WHITEPAPER.md not found."

def main():
    try:
        workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        repo_path = os.path.join(workspace, 'TOAI-elegant-lang')
        
        print(f"Scanning repository at: {repo_path}")
        
        git_commits = get_git_log(repo_path)
        whitepaper_summary = scan_whitepaper(repo_path)
        
        release_data = {
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "recent_commits": git_commits,
            "whitepaper_snippet": whitepaper_summary
        }
        
        output_dir = os.path.join(workspace, 'TOAI_Generated')
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, 'release_summary.json')
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(release_data, f, indent=2, ensure_ascii=False)
            
        print(f"Release summary successfully generated at: {output_file}")
        
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
