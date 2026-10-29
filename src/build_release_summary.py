# -*- coding: utf-8 -*-
import sys
import os
import traceback
import subprocess
import datetime
import json

def get_git_log(max_count=10):
    try:
        repo_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        git_path = os.path.join(repo_dir, 'TOAI-elegant-lang')
        if not os.path.exists(os.path.join(git_path, '.git')):
            git_path = repo_dir
            if not os.path.exists(os.path.join(git_path, '.git')):
                return "No git repository found."
        
        cmd = ['git', '-C', git_path, 'log', f'-n', str(max_count), '--pretty=format:%h - %an, %ar : %s']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout
    except Exception as e:
        return f"Error fetching git log: {str(e)}"

def scan_whitepapers():
    try:
        workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        papers = []
        for root, dirs, files in os.walk(workspace_dir):
            if '.git' in root:
                continue
            for file in files:
                if 'whitepaper' in file.lower() or file.endswith('.md'):
                    papers.append(os.path.join(root, file))
        return papers
    except Exception as e:
        return []

def main():
    try:
        print("Starting release summary generation...")
        git_history = get_git_log(15)
        whitepapers = scan_whitepapers()
        
        summary_data = {
            "timestamp": datetime.datetime.now().isoformat(),
            "git_log": git_history,
            "discovered_documents": whitepapers[:20]
        }
        
        workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
        os.makedirs(output_dir, exist_ok=True)
        
        output_path = os.path.join(output_dir, 'release_summary.json')
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, ensure_ascii=False, indent=2)
            
        print(f"Release summary successfully generated at: {output_path}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
