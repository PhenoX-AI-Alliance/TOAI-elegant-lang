import sys
import os
import traceback
import subprocess
import json
import datetime

def run_git_log():
    repo_path = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    git_dir = os.path.join(repo_path, '.git')
    if not os.path.exists(git_dir):
        return "Git repository not initialized or not found."
    try:
        result = subprocess.run(
            ['git', 'log', '-n', '10', '--oneline'],
            cwd=repo_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Error running git log: {e.stderr}"

def scan_whitepaper():
    repo_path = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    possible_paths = [
        os.path.join(repo_path, 'WHITEPAPER.md'),
        os.path.join(repo_path, 'TOAI-elegant-lang', 'WHITEPAPER.md'),
        os.path.join(repo_path, 'CONSTITUTION.md')
    ]
    content = ""
    for p in possible_paths:
        if os.path.exists(p):
            try:
                with open(p, 'r', encoding='utf-8') as f:
                    content += f"\n=== Source: {os.path.basename(p)} ===\n" + f.read()[:1000] + "\n"
            except Exception as ex:
                content += f"\nCould not read {p}: {str(ex)}\n"
    if not content:
        content = "No whitepaper or constitution found in standard paths."
    return content

def main():
    try:
        print("Starting release summary generation...")
        git_logs = run_git_log()
        whitepaper_snippet = scan_whitepaper()
        
        summary_data = {
            "timestamp": datetime.datetime.now().isoformat(),
            "git_recent_commits": git_logs,
            "whitepaper_summary": whitepaper_snippet
        }
        
        workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
        os.makedirs(output_dir, exist_ok=True)
        
        out_file = os.path.join(output_dir, 'release_summary.json')
        with open(out_file, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, ensure_ascii=False, indent=2)
            
        print(f"Release summary successfully generated at: {out_file}")
    except Exception as e:
        print(f"Critical error in release summary generation: {str(e)}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()\n