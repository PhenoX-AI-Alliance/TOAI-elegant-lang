import sys
import os
import traceback
import time
import json
import subprocess
import datetime

def get_git_logs():
    repo_path = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    git_dir = os.path.join(repo_path, 'TOAI-elegant-lang')
    if not os.path.exists(os.path.join(git_dir, '.git')):
        git_dir = repo_path
    
    try:
        result = subprocess.run(
            ['git', '-C', git_dir, 'log', '-n', '20', '--oneline'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except Exception as e:
        return f"Failed to retrieve git log: {str(e)}"

def scan_whitepaper():
    repo_path = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    search_dirs = [
        os.path.join(repo_path, 'TOAI-elegant-lang'),
        repo_path
    ]
    
    whitepaper_content = ""
    for d in search_dirs:
        for root, dirs, files in os.walk(d):
            if 'venv' in root or '.git' in root:
                continue
            for file in files:
                if 'whitepaper' in file.lower() or 'readme' in file.lower():
                    wp_path = os.path.join(root, file)
                    try:
                        with open(wp_path, 'r', encoding='utf-8') as f:
                            whitepaper_content += f"\n--- File: {wp_path} ---\n" + f.read()[:1000] + "\n"
                    except Exception:
                        pass
    if not whitepaper_content:
        whitepaper_content = "No whitepaper or README found in scan."
    return whitepaper_content

def main():
    try:
        workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
        os.makedirs(output_dir, exist_ok=True)
        
        git_logs = get_git_logs()
        whitepaper_summary = scan_whitepaper()
        
        now = datetime.datetime.now().isoformat()
        
        summary_data = {
            "timestamp": now,
            "git_logs": git_logs,
            "whitepaper_summary": whitepaper_summary
        }
        
        output_file = os.path.join(output_dir, 'release_summary.json')
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, ensure_ascii=False, indent=2)
            
        print(f"Successfully generated release summary at {output_file}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
