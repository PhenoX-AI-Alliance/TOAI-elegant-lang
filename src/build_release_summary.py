import sys
import os
import traceback
import time
import json
import subprocess
import datetime

def get_git_log():
    try:
        repo_path = os.getcwd()
        if not os.path.exists(os.path.join(repo_path, '.git')):
            subprocess.run(['git', 'init'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            subprocess.run(['git', 'config', 'user.name', 'TOAI Executor'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            subprocess.run(['git', 'config', 'user.email', 'executor@toai.local'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            subprocess.run(['git', 'add', '.'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            subprocess.run(['git', 'commit', '-m', 'Initial commit by TOAI Executor'], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        result = subprocess.run(
            ['git', 'log', '-n', '10', '--pretty=format:%h - %an, %ar : %s'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout
    except Exception as e:
        return f"Git log retrieval failed: {str(e)}"

def scan_whitepaper(workspace_dir):
    whitepaper_data = []
    try:
        for root, dirs, files in os.walk(workspace_dir):
            for file in files:
                if 'whitepaper' in file.lower() or file.endswith('.md'):
                    full_path = os.path.join(root, file)
                    whitepaper_data.append(full_path)
    except Exception as e:
        print(f"Error scanning files: {e}", file=sys.stderr)
    return whitepaper_data

def main():
    try:
        workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        git_logs = get_git_log()
        whitepapers = scan_whitepaper(workspace)
        
        summary = {
            "timestamp": datetime.datetime.now().isoformat(),
            "git_history": git_logs.splitlines(),
            "scanned_documents": whitepapers[:20],
            "version": "1.0.0",
            "status": "release_summary_generated"
        }
        
        output_dir = os.path.join(workspace, 'TOAI_Generated')
        os.makedirs(output_dir, exist_ok=True)
        
        output_file = os.path.join(output_dir, 'release_summary.json')
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
            
        print(f"Successfully generated release summary at {output_file}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
