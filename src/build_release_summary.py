import sys
import os
import traceback
import subprocess
import json
import datetime

def get_git_log(repo_path, max_count=20):
    try:
        cmd = ['git', '-C', repo_path, 'log', f'-n {max_count}', '--oneline']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip().split('\n')
    except Exception as e:
        return [f"Error fetching git log: {str(e)}"]

def scan_whitepaper(repo_path):
    whitepaper_path = os.path.join(repo_path, 'WHITEPAPER.md')
    if os.path.exists(whitepaper_path):
        try:
            with open(whitepaper_path, 'r', encoding='utf-8') as f:
                return f.read()[:1000] # Return first 1000 chars as summary
        except Exception as e:
            return f"Error reading whitepaper: {str(e)}"
    return "No WHITEPAPER.md found."

def main():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_path = os.path.join(workspace, 'TOAI-elegant-lang')
    
    print("Scanning repository for release summary...")
    logs = get_git_log(repo_path)
    whitepaper_summary = scan_whitepaper(repo_path)
    
    summary_data = {
        "timestamp": datetime.datetime.now().isoformat(),
        "git_logs": logs,
        "whitepaper_summary": whitepaper_summary
    }
    
    output_dir = os.path.join(workspace, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, 'release_summary.json')
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, indent=2, ensure_ascii=False)
        
    print(f"Release summary successfully generated at: {output_file}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)\n