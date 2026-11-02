import sys
import os
import traceback
import subprocess
import json
import datetime

def get_git_log(repo_path, max_count=20):
    try:
        result = subprocess.run(
            ['git', '-C', repo_path, 'log', f'-n', str(max_count), '--pretty=format:%h - %an, %ar : %s'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.splitlines()
    except subprocess.CalledProcessError as e:
        print(f"Git log error: {e.stderr}", file=sys.stderr)
        return []
    except Exception as e:
        print(f"Unexpected error fetching git log: {e}", file=sys.stderr)
        return []

def scan_whitepaper(repo_path):
    whitepaper_candidates = ['WHITEPAPER.md', 'README.md', 'docs/whitepaper.md']
    for candidate in whitepaper_candidates:
        full_path = os.path.join(repo_path, candidate)
        if os.path.exists(full_path):
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    return candidate, content[:1000]
            except Exception as e:
                print(f"Error reading {candidate}: {e}", file=sys.stderr)
    return None, "No whitepaper found."

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_path = os.path.join(workspace_dir, 'TOAI-elegant-lang')
    
    if not os.path.exists(repo_path):
        print(f"Repository path does not exist: {repo_path}", file=sys.stderr)
        sys.exit(1)
        
    git_dir = os.path.join(repo_path, '.git')
    if not os.path.exists(git_dir):
        print(f"Git repository not initialized at {repo_path}. Initializing...", file=sys.stdout)
        try:
            subprocess.run(['git', '-C', repo_path, 'init'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except Exception as e:
            print(f"Failed to initialize git repository: {e}", file=sys.stderr)
            
    logs = get_git_log(repo_path)
    wp_name, wp_snippet = scan_whitepaper(repo_path)
    
    summary = {
        "timestamp": datetime.datetime.now().isoformat(),
        "repository": "TOAI-elegant-lang",
        "whitepaper_source": wp_name,
        "whitepaper_snippet": wp_snippet,
        "recent_commits": logs
    }
    
    output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, 'release_summary.json')
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        print(f"Release summary successfully generated at: {output_file}")
    except Exception as e:
        print(f"Failed to write release summary: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
