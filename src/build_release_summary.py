import sys
import os
import traceback
import subprocess
import json
import datetime

def get_git_log(max_count=20):
    repo_dir = os.path.dirname(os.path.abspath(__file__))
    git_dir = os.path.join(repo_dir, '.git')
    if not os.path.exists(git_dir):
        parent_dir = os.path.dirname(repo_dir)
        if os.path.exists(os.path.join(parent_dir, '.git')):
            repo_dir = parent_dir
        else:
            return "Git repository not found."
            
    try:
        cmd = ['git', '-C', repo_dir, 'log', f'-n', str(max_count), '--pretty=format:%h - %an, %ar : %s']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout
    except Exception as e:
        return f"Failed to retrieve git log: {str(e)}"

def scan_whitepaper():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    search_paths = [
        workspace,
        os.path.join(workspace, 'TOAI-elegant-lang'),
        os.path.join(workspace, 'TOAI-elegant-lang', 'docs')
    ]
    
    whitepaper_content = "No whitepaper found."
    for path in search_paths:
        if os.path.exists(path):
            for filename in os.listdir(path):
                if 'whitepaper' in filename.lower() or 'hakusho' in filename.lower() or 'policy' in filename.lower():
                    full_path = os.path.join(path, filename)
                    if os.path.isfile(full_path):
                        try:
                            with open(full_path, 'r', encoding='utf-8') as f:
                                whitepaper_content = f.read()[:2000]
                                break
                        except Exception:
                            pass
        if whitepaper_content != "No whitepaper found.":
            break
            
    return whitepaper_content

def main():
    try:
        print("Starting release summary generation...")
        git_history = get_git_log()
        whitepaper = scan_whitepaper()
        
        summary_data = {
            "timestamp": datetime.datetime.now().isoformat(),
            "git_log": git_history,
            "whitepaper_excerpt": whitepaper
        }
        
        workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        output_dir = os.path.join(workspace, 'TOAI_Generated')
        os.makedirs(output_dir, exist_ok=True)
        
        output_path = os.path.join(output_dir, 'release_summary.json')
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, ensure_ascii=False, indent=2)
            
        print(f"Release summary successfully written to {output_path}")
        
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
