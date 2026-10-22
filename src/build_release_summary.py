# -*- coding: utf-8 -*-
import sys
import os
import traceback
import time
import json
import subprocess
from datetime import datetime

def get_git_log():
    repo_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    git_path = os.path.join(repo_dir, '.git')
    if not os.path.exists(git_path):
        return "Git repository not initialized or not found."
    try:
        result = subprocess.run(
            ['git', 'log', '-n', '10', '--oneline'],
            cwd=repo_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Error fetching git log: {e.stderr}"
    except Exception as e:
        return f"Unexpected error in git log: {str(e)}"

def scan_whitepaper():
    repo_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    target_paths = [
        os.path.join(repo_dir, 'WHITEPAPER.md'),
        os.path.join(repo_dir, 'CONSTITUTION.md'),
        os.path.join(repo_dir, 'README.md')
    ]
    summary_data = {}
    for path in target_paths:
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    title = lines[0].strip() if lines else "No Title"
                    summary_data[os.path.basename(path)] = {
                        "title": title,
                        "line_count": len(lines)
                    }
            except Exception as e:
                summary_data[os.path.basename(path)] = {"error": str(e)}
        else:
            summary_data[os.path.basename(path)] = {"status": "not found"}
    return summary_data

def build_summary():
    try:
        git_history = get_git_log()
        whitepaper_info = scan_whitepaper()
        
        release_data = {
            "timestamp": datetime.now().isoformat(),
            "version": "1.0.0-gaia",
            "git_log": git_history,
            "documents": whitepaper_info
        }
        
        output_dir = os.path.join(os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/'), 'TOAI_Generated')
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, 'release_summary.json')
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(release_data, f, ensure_ascii=False, indent=2)
            
        print(f"Release summary successfully built at: {output_file}")
    except Exception as e:
        print(f"Error in build_summary: {str(e)}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    build_summary()
