import sys
import os
import traceback
import subprocess
import datetime
import json

def get_git_log(repo_path, max_count=20):
    try:
        result = subprocess.run(
            ['git', '-C', repo_path, 'log', f'-n {max_count}', '--pretty=format:%h - %an: %s (%ad)'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except Exception as e:
        return f"Could not fetch git log: {str(e)}"

def scan_whitepaper(repo_path):
    wp_path = os.path.join(repo_path, 'WHITE_PAPER.md')
    if os.path.exists(wp_path):
        try:
            with open(wp_path, 'r', encoding='utf-8') as f:
                content = f.read()
                return content[:1000] + "\n...[truncated]..." if len(content) > 1000 else content
        except Exception as e:
            return f"Error reading WHITE_PAPER.md: {str(e)}"
    return "WHITE_PAPER.md not found."

def main():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_path = os.path.join(workspace, 'TOAI-elegant-lang')
    
    if not os.path.exists(repo_path):
        print(f"Error: Repository path does not exist: {repo_path}")
        sys.exit(1)
        
    git_status = "Not a git repository"
    if os.path.exists(os.path.join(repo_path, '.git')):
        git_status = get_git_log(repo_path)
    else:
        print("Warning: .git directory not found in repository path.")
        
    whitepaper_summary = scan_whitepaper(repo_path)
    
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    summary_data = {
        "timestamp": timestamp,
        "repository": "TOAI-elegant-lang",
        "git_log": git_status,
        "whitepaper_excerpt": whitepaper_summary
    }
    
    output_dir = os.path.join(workspace, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'release_summary.json')
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, ensure_ascii=False, indent=4)
        print(f"Release summary successfully built at: {output_path}")
    except Exception as e:
        print(f"Error writing release summary: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()
