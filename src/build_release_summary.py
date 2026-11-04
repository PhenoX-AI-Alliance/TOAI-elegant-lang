import sys
import os
import traceback
import subprocess
import json
from datetime import datetime

def get_git_log(repo_path, max_count=20):
    try:
        cmd = ['git', '-C', repo_path, 'log', f'-n', str(max_count), '--pretty=format:%h - %an, %ar : %s']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Error fetching git log: {str(e)}"]

def main():
    try:
        workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        repo_path = os.path.join(workspace_dir, 'TOAI-elegant-lang')
        output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
        os.makedirs(output_dir, exist_ok=True)
        
        logs = get_git_log(repo_path)
        
        summary_data = {
            "timestamp": datetime.now().isoformat(),
            "repository": "TOAI-elegant-lang",
            "recent_commits": logs
        }
        
        output_file = os.path.join(output_dir, 'release_summary.json')
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, ensure_ascii=False, indent=2)
            
        print(f"Successfully generated release summary at: {output_file}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()