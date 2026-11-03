import sys
import os
import subprocess
import json
from datetime import datetime

def get_git_log():
    try:
        result = subprocess.run(
            ['git', 'log', '-n', '10', '--pretty=format:%h - %an: %s (%ad)'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Git log unavailable: {str(e)}"]

def scan_whitepapers(workspace_dir):
    docs = []
    whitepaper_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang')
    if os.path.exists(whitepaper_dir):
        for root, dirs, files in os.walk(whitepaper_dir):
            for file in files:
                if file.endswith('.md') or file.endswith('.txt'):
                    docs.append(os.path.join(root, file))
    return docs

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    
    git_commits = get_git_log()
    whitepapers = scan_whitepapers(workspace_dir)
    
    summary = {
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "recent_commits": git_commits,
        "scanned_documents": whitepapers
    }
    
    output_path = os.path.join(output_dir, 'release_summary.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
        
    print(f"Successfully generated release summary at: {output_path}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"Error in release summary builder: {e}", file=sys.stderr)
        sys.exit(1)