import sys
import os
import traceback
import time
import json
import subprocess
import datetime

def get_git_log():
    try:
        repo_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        TOAI_elegant_dir = os.path.join(repo_dir, 'TOAI-elegant-lang')
        if not os.path.exists(os.path.join(TOAI_elegant_dir, '.git')):
            # Fallback to workspace root if TOAI-elegant-lang is not its own repo
            TOAI_elegant_dir = repo_dir
            
        result = subprocess.run(
            ['git', 'log', '-n', '20', '--pretty=format:%h - %an, %ar : %s'],
            cwd=TOAI_elegant_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout
    except Exception as e:
        return f"Could not retrieve git log: {str(e)}"

def scan_whitepaper():
    try:
        repo_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        docs_path = os.path.join(repo_dir, 'TOAI-elegant-lang', 'docs')
        if not os.path.exists(docs_path):
            docs_path = os.path.join(repo_dir, 'docs')
            
        whitepaper_files = []
        if os.path.exists(docs_path):
            for root, dirs, files in os.walk(docs_path):
                for file in files:
                    if 'whitepaper' in file.lower() or file.endswith('.md'):
                        whitepaper_files.append(os.path.join(root, file))
        return whitepaper_files
    except Exception as e:
        return [f"Error scanning whitepapers: {str(e)}"]

def main():
    try:
        workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
        os.makedirs(output_dir, exist_ok=True)
        
        git_log_data = get_git_log()
        whitepapers = scan_whitepaper()
        
        summary = {
            "timestamp": datetime.datetime.now().isoformat(),
            "git_log": git_log_data,
            "whitepapers_found": whitepapers,
            "version": "1.0.0-alpha"
        }
        
        output_file = os.path.join(output_dir, 'release_summary.json')
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
            
        print(f"Successfully generated release summary at {output_file}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
