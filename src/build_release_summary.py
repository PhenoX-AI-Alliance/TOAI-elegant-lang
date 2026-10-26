import sys
import os
import subprocess
import json
import traceback

def get_git_log():
    try:
        repo_path = os.path.dirname(os.path.abspath(__file__))
        result = subprocess.run(
            ['git', 'log', '-n', '10', '--oneline'],
            cwd=repo_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.strip().split('\n')
    except Exception as e:
        return [f"Git log unavailable: {str(e)}"]

def scan_whitepaper():
    try:
        repo_path = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(repo_path)
        wp_path = os.path.join(parent_dir, 'WHITE_PAPER.md')
        if os.path.exists(wp_path):
            with open(wp_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            return ''.join(lines[:20])
        return "Whitepaper not found."
    except Exception as e:
        return f"Error reading whitepaper: {str(e)}"

def main():
    print("Building release summary...")
    logs = get_git_log()
    wp_summary = scan_whitepaper()
    
    summary_data = {
        "version": "1.0.0",
        "git_recent_commits": logs,
        "whitepaper_excerpt": wp_summary
    }
    
    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'release_summary.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, ensure_ascii=False, indent=2)
    
    print(f"Release summary successfully written to {output_path}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
