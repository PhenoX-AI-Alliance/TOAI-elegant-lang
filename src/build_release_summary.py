import sys
import os
import traceback
import subprocess
import json
import datetime

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
        return [f"Git log retrieval failed: {str(e)}"]

def scan_whitepapers(workspace_dir):
    whitepapers = []
    target_path = os.path.join(workspace_dir, 'TOAI-elegant-lang')
    if os.path.exists(target_path):
        for root, dirs, files in os.walk(target_path):
            for file in files:
                if 'whitepaper' in file.lower() or file.endswith('.md'):
                    whitepapers.path = os.path.join(root, file)
                    whitepapers.append(os.path.relpath(whitepapers.path, workspace_dir))
    return whitepapers

def main():
    try:
        workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
        os.makedirs(output_dir, exist_ok=True)
        
        git_logs = get_git_log()
        whitepapers = scan_whitepapers(workspace_dir)
        
        summary = {
            "timestamp": datetime.datetime.now().isoformat(),
            "git_recent_commits": git_logs,
            "detected_documents": whitepapers
        }
        
        output_file = os.path.join(output_dir, 'release_summary.json')
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
            
        print(f"Release summary successfully built at: {output_file}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
