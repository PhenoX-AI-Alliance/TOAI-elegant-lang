import sys
import os
import subprocess
import json
import datetime

def get_git_log(max_count=10):
    try:
        cmd = ['git', 'log', f'-n', str(max_count), '--pretty=format:%h - %an, %ar : %s']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Git log unavailable: {str(e)}"]

def scan_whitepaper():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    candidates = [
        os.path.join(workspace_dir, 'WHITEPAPER.md'),
        os.path.join(workspace_dir, 'CONSTITUTION.md'),
        os.path.join(workspace_dir, 'TOAI-elegant-lang', 'README.md')
    ]
    summary = {}
    for path in candidates:
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    summary[os.path.basename(path)] = content[:300] + "..." if len(content) > 300 else content
            except Exception as e:
                summary[os.path.basename(path)] = f"Error reading: {str(e)}"
    return summary

def generate_release_summary():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    output_path = os.path.join(workspace_dir, 'TOAI_Generated', 'release_summary.json')
    
    git_commits = get_git_log(15)
    whitepaper_snippets = scan_whitepaper()
    
    data = {
        "timestamp": datetime.datetime.now().isoformat(),
        "version": "1.0.0-gaia",
        "recent_commits": git_commits,
        "whitepaper_snippets": whitepaper_snippets
    }
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Successfully generated release summary at: {output_path}")
    except Exception as e:
        print(f"Failed to write release summary: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    generate_release_summary()
