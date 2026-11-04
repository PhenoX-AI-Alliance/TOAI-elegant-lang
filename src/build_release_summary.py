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
        return f"Could not retrieve git log: {str(e)}"

def scan_whitepaper(repo_path):
    wp_path = os.path.join(repo_path, 'WHITEPAPER.md')
    if os.path.exists(wp_path):
        try:
            with open(wp_path, 'r', encoding='utf-8') as f:
                content = f.read()
                return content[:1000] + "... [truncated]"
        except Exception as e:
            return f"Error reading WHITEPAPER.md: {str(e)}"
    return "WHITEPAPER.md not found in repository."

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_path = os.path.join(workspace_dir, 'TOAI-elegant-lang')
    
    print(f"Scanning repository at: {repo_path}")
    
    git_log_output = get_git_log(repo_path)
    whitepaper_summary = scan_whitepaper(repo_path)
    
    summary_data = {
        "timestamp": datetime.datetime.now().isoformat(),
        "repository": "TOAI-elegant-lang",
        "git_log": git_log_output,
        "whitepaper_excerpt": whitepaper_summary
    }
    
    output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, 'release_summary.json')
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, ensure_ascii=False, indent=2)
        print(f"Release summary successfully generated at: {output_file}")
    except Exception as e:
        print(f"Failed to write release summary: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
