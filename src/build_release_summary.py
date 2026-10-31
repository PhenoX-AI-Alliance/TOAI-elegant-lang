import sys
import os
import traceback
import subprocess
import json
import datetime

def get_git_logs(repo_path, max_count=20):
    try:
        result = subprocess.run(
            ['git', '-C', repo_path, 'log', f'-n {max_count}', '--pretty=format:%h - %an, %ar : %s'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Git log retrieval failed: {str(e)}"]

def scan_whitepaper(repo_path):
    whitepaper_candidates = [
        os.path.join(repo_path, 'WHITEPAPER.md'),
        os.path.join(repo_path, 'docs', 'WHITEPAPER.md'),
        os.path.join(repo_path, 'README.md')
    ]
    for path in whitepaper_candidates:
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    return f.read()[:2000] # return first 2000 chars as summary
            except Exception:
                pass
    return "No whitepaper found."

def main():
    try:
        workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        repo_path = os.path.join(workspace, 'TOAI-elegant-lang')
        
        if not os.path.exists(os.path.join(repo_path, '.git')):
            print("Target directory is not a git repository. Initializing...")
            subprocess.run(['git', 'init', repo_path], check=True)
            
        logs = get_git_logs(repo_path)
        whitepaper_summary = scan_whitepaper(repo_path)
        
        summary_data = {
            "timestamp": datetime.datetime.now().isoformat(),
            "git_logs": logs,
            "whitepaper_summary": whitepaper_summary
        }
        
        output_json_path = os.path.join(workspace, 'TOAI_Generated', 'release_summary.json')
        with open(output_json_path, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, ensure_ascii=False, indent=2)
            
        print(f"Successfully generated release summary at: {output_json_path}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
