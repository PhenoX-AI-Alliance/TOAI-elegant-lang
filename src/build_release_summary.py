import sys
import os
import subprocess
import json
import datetime
import traceback

def get_git_log():
    try:
        if not os.path.exists('.git'):
            return "Git repository not initialized."
        result = subprocess.run(
            ['git', 'log', '-n', '10', '--pretty=format:%h - %an, %ar : %s'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout
    except Exception as e:
        return f"Could not retrieve git log: {str(e)}"

def scan_whitepaper():
    candidates = ['whitepaper.md', 'WHITE_PAPER.md', 'README.md']
    for c in candidates:
        if os.path.exists(c):
            try:
                with open(c, 'r', encoding='utf-8') as f:
                    content = f.read(2000)
                    return f"Found {c}:\n{content[:500]}..."
            except Exception as e:
                continue
    return "No whitepaper found."

def main():
    print("Building release summary...")
    git_history = get_git_log()
    whitepaper_summary = scan_whitepaper()
    
    summary = {
        "timestamp": datetime.datetime.now().isoformat(),
        "git_log": git_history,
        "whitepaper_excerpt": whitepaper_summary
    }
    
    output_path = os.path.join(os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/'), 'TOAI_Generated', 'release_summary.json')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
        
    print(f"Release summary successfully written to {output_path}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
