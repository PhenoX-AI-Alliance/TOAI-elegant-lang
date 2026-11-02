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
            ['git', 'log', f'-n', str(max_count), '--pretty=format:%h - %an, %ar : %s'],
            cwd=repo_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.splitlines()
    except Exception as e:
        print(f"Warning: Could not fetch git log: {e}")
        return []

def scan_whitepaper(workspace_path):
    whitepaper_candidates = [
        os.path.join(workspace_path, 'WHITEPAPER.md'),
        os.path.join(workspace_path, 'CONSTITUTION.md'),
        os.path.join(workspace_path, 'TOAI-elegant-lang', 'WHITEPAPER.md')
    ]
    for path in whitepaper_candidates:
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    return path, f.read()[:2000]
            except Exception as e:
                print(f"Warning: Could not read {path}: {e}")
    return None, "No whitepaper found."

def main():
    try:
        workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        repo_path = os.path.join(workspace_dir, 'TOAI-elegant-lang')
        
        if not os.path.exists(os.path.join(repo_path, '.git')):
            print(f"Initializing git repository at {repo_path}")
            os.makedirs(repo_path, exist_ok=True)
            subprocess.run(['git', 'init'], cwd=repo_path, check=True)
            subprocess.run(['git', 'config', 'user.name', 'TOAI Builder'], cwd=repo_path, check=True)
            subprocess.run(['git', 'config', 'user.email', 'builder@toai.ecosystem'], cwd=repo_path, check=True)
            
        logs = get_git_log(repo_path)
        wp_path, wp_content = scan_whitepaper(workspace_dir)
        
        summary = {
            "timestamp": datetime.datetime.now().isoformat(),
            "repository": repo_path,
            "git_logs": logs,
            "whitepaper_source": wp_path,
            "whitepaper_excerpt": wp_content[:500]
        }
        
        output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, 'release_summary.json')
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
            
        print(f"Successfully generated release summary at {output_file}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
