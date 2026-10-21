import os
import sys
import subprocess
import json
import datetime
import traceback

def run_git_log():
    try:
        repo_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if not os.path.exists(os.path.join(repo_path, '.git')):
            return "Git repository not initialized or found."
        
        result = subprocess.run(
            ['git', 'log', '-n', '10', '--pretty=format:%h - %an, %ar : %s'],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except Exception as e:
        return f"Could not retrieve git log: {str(e)}"

def scan_whitepaper(workspace_dir):
    try:
        whitepaper_path = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'WHITESPAPER.md')
        if os.path.exists(whitepaper_path):
            with open(whitepaper_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.splitlines()
                return lines[:20]
        return ["Whitepaper not found."]
    except Exception as e:
        return [f"Error reading whitepaper: {str(e)}"]

def main():
    try:
        workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        git_history = run_git_log()
        whitepaper_summary = scan_whitepaper(workspace_dir)
        
        release_data = {
            "timestamp": datetime.datetime.now().isoformat(),
            "git_log": git_history.splitlines(),
            "whitepaper_summary": whitepaper_summary
        }
        
        output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, 'release_summary.json')
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(release_data, f, ensure_ascii=False, indent=2)
            
        print(f"Release summary successfully built at: {output_file}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
