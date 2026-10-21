import sys
import os
import subprocess
import json
import datetime

def get_git_log(limit=10):
    try:
        result = subprocess.run(
            ['git', 'log', f'-n {limit}', '--pretty=format:%h - %an: %s (%ad)'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.strip().split('\n')
    except Exception as e:
        return [f"Git log unavailable: {str(e)}"]

def scan_whitepaper(workspace_dir):
    whitepaper_paths = [
        os.path.join(workspace_dir, 'WHITEPAPER.md'),
        os.path.join(workspace_dir, 'TOAI-elegant-lang', 'WHITEPAPER.md'),
        os.path.join(workspace_dir, 'CONSTITUTION.md')
    ]
    summaries = []
    for path in whitepaper_paths:
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    title = lines[0].strip() if lines else "No Title"
                    summaries.append({"path": path, "title": title, "lines_count": len(lines)})
            except Exception as e:
                summaries.append({"path": path, "error": str(e)})
    return summaries

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    os.chdir(workspace_dir)
    
    git_history = get_git_log(15)
    whitepaper_info = scan_whitepaper(workspace_dir)
    
    release_data = {
        "timestamp": datetime.datetime.now().isoformat(),
        "version": "1.0.0-gaia",
        "git_commits": git_history,
        "documents": whitepaper_info
    }
    
    output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'release_summary.json')
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(release_data, f, ensure_ascii=False, indent=2)
    
    print(f"Successfully generated release summary at: {output_path}")

if __name__ == '__main__':
    main()
