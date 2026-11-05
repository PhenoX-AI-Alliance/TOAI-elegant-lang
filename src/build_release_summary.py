import sys
import os
import traceback
import subprocess
import datetime
import json

def get_git_log():
    try:
        repo_path = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        git_dir = os.path.join(repo_path, '.git')
        if not os.path.exists(git_dir):
            return "Git repository not initialized."
        
        result = subprocess.run(
            ['git', 'log', '-n', '10', '--oneline'],
            cwd=repo_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout
    except Exception as e:
        return f"Error fetching git log: {str(e)}"

def scan_whitepaper():
    try:
        workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        potential_paths = [
            os.path.join(workspace, 'WHITE_PAPER.md'),
            os.path.join(workspace, 'docs', 'WHITE_PAPER.md'),
            os.path.join(workspace, 'TOAI-elegant-lang', 'WHITE_PAPER.md')
        ]
        for path in potential_paths:
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    return f.read()[:1000] # Return first 1000 chars as summary
        return "Whitepaper not found."
    except Exception as e:
        return f"Error reading whitepaper: {str(e)}"

def generate_release_summary():
    try:
        workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        output_file = os.path.join(workspace, 'TOAI_Generated', 'release_summary.json')
        
        git_log = get_git_log()
        whitepaper_summary = scan_whitepaper()
        
        summary_data = {
            "timestamp": datetime.datetime.now().isoformat(),
            "git_recent_commits": git_log,
            "whitepaper_excerpt": whitepaper_summary,
            "status": "success"
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, ensure_ascii=False, indent=2)
            
        print(f"Release summary successfully generated at {output_file}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    generate_release_summary()
