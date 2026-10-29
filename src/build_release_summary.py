import sys
import os
import subprocess
import json
import glob
from datetime import datetime

def main():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    repo_path = os.path.join(workspace, 'TOAI-elegant-lang')
    
    print("[INFO] Starting release summary generation...")
    
    git_logs = "No git history available."
    if os.path.exists(os.path.join(repo_path, '.git')):
        try:
            result = subprocess.run(
                ['git', '-C', repo_path, 'log', '-n', '10', '--oneline'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )
            git_logs = result.stdout
        except Exception as e:
            print(f"[WARNING] Failed to fetch git log: {e}")
    else:
        print("[WARNING] Target directory is not a git repository.")

    whitepaper_files = glob.glob(os.path.join(workspace, '**', '*.md'), recursive=True)
    whitepaper_summary = []
    for wf in whitepaper_files[:5]:
        try:
            with open(wf, 'r', encoding='utf-8') as f:
                header = f.readline().strip()
                whitepaper_summary.append({"file": wf, "header": header})
        except Exception:
            pass

    summary_data = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "git_logs": git_logs.splitlines(),
        "whitepapers": whitepaper_summary
    }

    output_path = os.path.join(repo_path, 'release_summary.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, ensure_ascii=False, indent=2)
        
    print(f"[SUCCESS] Release summary successfully written to {output_path}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)
