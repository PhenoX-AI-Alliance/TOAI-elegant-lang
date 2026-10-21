import sys
import os
import traceback
import subprocess
import datetime
import json

def get_git_log(repo_path, max_count=10):
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
        return [f"Git log retrieval failed: {str(e)}"]

def scan_whitepapers(repo_path):
    docs = []
    try:
        for root, dirs, files in os.walk(repo_path):
            for file in files:
                if 'whitepaper' in file.lower() or file.endswith('.md'):
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, repo_path)
                    docs.append(rel_path)
    except Exception as e:
        print(f"Error scanning whitepapers: {e}")
    return docs

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_path = os.path.join(workspace_dir, 'TOAI-elegant-lang')
    
    print(f"Scanning repository at: {repo_path}")
    
    logs = get_git_log(repo_path)
    whitepapers = scan_whitepapers(repo_path)
    
    summary = {
        "timestamp": datetime.datetime.now().isoformat(),
        "repository": "TOAI-elegant-lang",
        "recent_commits": logs,
        "documentation_files": whitepapers
    }
    
    output_path = os.path.join(workspace_dir, 'TOAI_Generated', 'release_summary.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
        
    print(f"Release summary successfully generated at: {output_path}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
