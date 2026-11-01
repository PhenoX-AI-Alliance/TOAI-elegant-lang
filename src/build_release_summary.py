import sys
import os
import traceback
import time
import json
import subprocess
import datetime

def get_git_log(repo_path, max_count=20):
    try:
        result = subprocess.run(
            ['git', 'log', f'-n {max_count}', '--pretty=format:%h - %an: %s (%ad)'],
            cwd=repo_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except Exception as e:
        return f"Error fetching git log: {str(e)}"

def scan_whitepaper(repo_path):
    whitepaper_candidates = [
        os.path.join(repo_path, 'WHITE_PAPER.md'),
        os.path.join(repo_path, 'docs', 'WHITE_PAPER.md'),
        os.path.join(repo_path, 'README.md')
    ]
    for path in whitepaper_candidates:
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    return path, f.read()[:2000]
            except Exception as e:
                pass
    return None, "No whitepaper or README found."

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_path = os.path.join(workspace_dir, 'TOAI-elegant-lang')
    
    if not os.path.exists(repo_path):
        print(f"Repository path does not exist: {repo_path}")
        sys.exit(1)
        
    git_dir = os.path.join(repo_path, '.git')
    if not os.path.exists(git_dir):
        print("Git repository not initialized. Initializing for release summary...")
        try:
            subprocess.run(['git', 'init'], cwd=repo_path, check=True)
            subprocess.run(['git', 'config', 'user.name', 'TOAI Release Agent'], cwd=repo_path, check=True)
            subprocess.run(['git', 'config', 'user.email', 'agent@toai.local'], cwd=repo_path, check=True)
        except Exception as e:
            print(f"Failed to initialize git: {e}")
            
    logs = get_git_log(repo_path)
    wp_path, wp_content = scan_whitepaper(repo_path)
    
    summary = {
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "repository": "TOAI-elegant-lang",
        "git_log": logs,
        "whitepaper_source": wp_path,
        "whitepaper_excerpt": wp_content
    }
    
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
        traceback.print_exc()
        sys.exit(1)
