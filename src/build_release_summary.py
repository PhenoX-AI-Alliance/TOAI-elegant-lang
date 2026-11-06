import sys
import os
import traceback
import subprocess
import json
from datetime import datetime

def get_git_log(max_count=20):
    try:
        repo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        result = subprocess.run(
            ['git', 'log', f'-n {max_count}', '--pretty=format:%h - %an, %ad : %s'],
            cwd=repo_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Git log retrieval failed: {str(e)}"]

def scan_whitepaper():
    try:
        repo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        wp_path = os.path.join(repo_path, 'WHITEPAPER.md')
        if os.path.exists(wp_path):
            with open(wp_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            return [line.strip() for line in lines[:10] if line.strip()]
        return ["Whitepaper not found."]
    except Exception as e:
        return [f"Whitepaper scan failed: {str(e)}"]

def main():
    try:
        workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
        os.makedirs(output_dir, exist_ok=True)
        
        git_logs = get_git_log()
        whitepaper_summary = scan_whitepaper()
        
        release_data = {
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0-gaia",
            "git_history": git_logs,
            "whitepaper_glance": whitepaper_summary
        }
        
        output_file = os.path.join(output_dir, 'release_summary.json')
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(release_data, f, ensure_ascii=False, indent=2)
            
        print(f"Successfully generated release summary at: {output_file}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
