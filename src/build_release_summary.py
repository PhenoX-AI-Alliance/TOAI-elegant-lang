import sys
import os
import traceback
import subprocess
import json
import datetime

def get_git_log(max_count=10):
    repo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    try:
        result = subprocess.run(
            ['git', 'log', f'-n', str(max_count), '--pretty=format:%h - %an, %ar : %s'],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.splitlines()
    except Exception as e:
        print(f"Warning: Could not fetch git log: {e}")
        return []

def scan_whitepapers():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    docs_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang')
    found_files = []
    try:
        if os.path.exists(docs_dir):
            for root, dirs, files in os.walk(docs_dir):
                for file in files:
                    if 'whitepaper' in file.lower() or file.endswith('.md'):
                        found_files.append(os.path.join(root, file))
    except Exception as e:
        print(f"Warning: Could not scan whitepapers: {e}")
    return found_files

def main():
    print("=== TOAI Release Summary Builder ===")
    logs = get_git_log(15)
    whitepapers = scan_whitepapers()
    
    summary = {
        "timestamp": datetime.datetime.now().isoformat(),
        "recent_commits": logs,
        "related_documents": whitepapers
    }
    
    output_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    output_path = os.path.join(output_dir, 'TOAI_Generated', 'release_summary.json')
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
        
    print(f"Release summary successfully generated at: {output_path}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
