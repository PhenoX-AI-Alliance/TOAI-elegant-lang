import sys
import os
import traceback
import subprocess
import json
import datetime

def run_git_log():
    try:
        repo_path = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        git_dir = os.path.join(repo_path, '.git')
        if not os.path.exists(git_dir):
            return "Git repository not found at target path."
        
        result = subprocess.run(
            ['git', 'log', '-n', '10', '--pretty=format:%h - %an, %ar : %s'],
            cwd=repo_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout
    except Exception as e:
        return f"Failed to retrieve git log: {str(e)}"

def scan_whitepaper():
    try:
        workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        whitepaper_path = os.path.join(workspace, 'WHITE_PAPER.md')
        if os.path.exists(whitepaper_path):
            with open(whitepaper_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return content[:1000] + "\n... [Truncated]"
        return "Whitepaper not found."
    except Exception as e:
        return f"Failed to read whitepaper: {str(e)}"

def main():
    try:
        workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        output_dir = os.path.join(workspace, 'TOAI_Generated')
        os.makedirs(output_dir, exist_ok=True)
        
        git_summary = run_git_log()
        whitepaper_summary = scan_whitepaper()
        
        report = {
            "timestamp": datetime.datetime.now().isoformat(),
            "git_log": git_summary,
            "whitepaper_excerpt": whitepaper_summary
        }
        
        output_file = os.path.join(output_dir, 'release_summary.json')
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
            
        print(f"Release summary successfully built at: {output_file}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
