import sys
import os
import traceback
import time
import json
import subprocess
from datetime import datetime

def get_git_log(repo_path, max_count=20):
    try:
        result = subprocess.run(
            ['git', '-C', repo_path, 'log', f'-n {max_count}', '--pretty=format:%h - %an, %ar : %s'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except Exception as e:
        return f"Git log retrieval failed: {str(e)}"

def scan_whitepaper(repo_path):
    wp_path = os.path.join(repo_path, 'WHITE_PAPER.md')
    if os.path.exists(wp_path):
        try:
            with open(wp_path, 'r', encoding='utf-8') as f:
                return f.read()[:2000]
        except Exception as e:
            return f"Failed to read WHITE_PAPER.md: {str(e)}"
    return "WHITE_PAPER.md not found."

def main():
    try:
        workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        repo_path = os.path.join(workspace_dir, 'TOAI-elegant-lang')
        
        if not os.path.exists(os.path.join(repo_path, '.git')):
            print("Git repository not initialized. Initializing for summary generation...")
            subprocess.run(['git', 'init', repo_path], check=True)
            subprocess.run(['git', '-C', repo_path, 'config', 'user.name', 'TOAI Executor'], check=True)
            subprocess.run(['git', '-C', repo_path, 'config', 'user.email', 'executor@toai.internal'], check=True)
            # Create an initial commit if none exists
            readme_path = os.path.join(repo_path, 'README.md')
            if not os.path.exists(readme_path):
                with open(readme_path, 'w', encoding='utf-8') as f:
                    f.write("# TOAI Elegant Lang\n")
            subprocess.run(['git', '-C', repo_path, 'add', '.'], check=True)
            subprocess.run(['git', '-C', repo_path, 'commit', '-m', 'Initial commit for release summary'], check=True)

        git_logs = get_git_log(repo_path)
        whitepaper_content = scan_whitepaper(repo_path)
        
        summary_data = {
            "timestamp": datetime.now().isoformat(),
            "git_logs": git_logs,
            "whitepaper_excerpt": whitepaper_content
        }
        
        output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, 'release_summary.json')
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, ensure_ascii=False, indent=2)
            
        print(f"Release summary successfully built at: {output_path}")
        
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
