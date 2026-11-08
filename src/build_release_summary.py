import sys
import os
import traceback
import subprocess
import json
import datetime

def get_git_log():
    try:
        repo_path = os.path.dirname(os.path.abspath(__file__))
        result = subprocess.run(
            ['git', 'log', '-n', '10', '--oneline'],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except Exception as e:
        return f"Git log retrieval failed: {str(e)}"

def main():
    try:
        workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        output_dir = os.path.join(workspace, 'TOAI_Generated')
        os.makedirs(output_dir, exist_ok=True)
        
        git_history = get_git_log()
        now_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        summary_data = {
            "timestamp": now_str,
            "version": "1.0.0",
            "git_recent_commits": git_history.splitlines(),
            "status": "release_summary_generated"
        }
        
        out_file = os.path.join(output_dir, 'release_summary.json')
        with open(out_file, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, ensure_ascii=False, indent=2)
            
        print(f"Successfully generated release summary at {out_file}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
