import sys
import os
import traceback
import subprocess
import datetime
import json

def get_git_logs():
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

def scan_whitepaper():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    whitepaper_candidates = [
        os.path.join(workspace_dir, 'WHITEPAPER.md'),
        os.path.join(workspace_dir, 'TOAI-elegant-lang', 'WHITEPAPER.md')
    ]
    for path in whitepaper_candidates:
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    return ''.join(lines[:30])
            except Exception:
                pass
    return "Whitepaper not found."

def main():
    try:
        workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
        os.makedirs(output_dir, exist_ok=True)
        
        logs = get_git_logs()
        whitepaper_summary = scan_whitepaper()
        
        release_data = {
            "timestamp": datetime.datetime.now().isoformat(),
            "git_logs": logs,
            "whitepaper_excerpt": whitepaper_summary
        }
        
        output_path = os.path.join(output_dir, 'release_summary.json')
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(release_data, f, ensure_ascii=False, indent=2)
            
        print(f"Successfully generated release summary at: {output_path}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
