import sys
import os
import subprocess
import json
import datetime

def get_git_log(max_count=20):
    try:
        repo_path = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        git_dir = os.path.join(repo_path, '.git')
        if not os.path.exists(git_dir):
            return "Git repository not initialized."
        
        cmd = ['git', '-C', repo_path, 'log', f'-n {max_count}', '--pretty=format:%h - %an, %ar : %s']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout
    except Exception as e:
        return f"Error fetching git log: {str(e)}"

def scan_whitepaper():
    try:
        workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        candidates = [
            os.path.join(workspace, 'WHITE_PAPER.md'),
            os.path.join(workspace, 'CONSTITUTION.md'),
            os.path.join(workspace, 'README.md')
        ]
        summary = {}
        for path in candidates:
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    summary[os.path.basename(path)] = content[:500] + "..." if len(content) > 500 else content
        return summary
    except Exception as e:
        return {"error": str(e)}

def build_summary():
    timestamp = datetime.datetime.now().isoformat()
    git_history = get_git_log()
    docs = scan_whitepaper()
    
    report = {
        "timestamp": timestamp,
        "version": "1.0.0-gaia",
        "git_log": git_history,
        "documents_scanned": docs
    }
    
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    out_file = os.path.join(workspace, 'TOAI_Generated', 'release_summary.json')
    
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    print(f"Release summary successfully built at: {out_file}")

if __name__ == '__main__':
    build_summary()
