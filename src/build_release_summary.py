# -*- coding: utf-8 -*-
import sys
import os
import traceback
import subprocess
import json
import datetime

def get_git_log(max_count=10):
    try:
        repo_dir = os.path.dirname(os.path.abspath(__file__))
        cmd = ['git', '-C', repo_dir, 'log', f'-n {max_count}', '--pretty=format:%h - %an, %ar : %s']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Git log retrieval failed: {str(e)}"]

def scan_whitepapers(workspace_dir):
    whitepapers = []
    try:
        for root, dirs, files in os.walk(workspace_dir):
            for file in files:
                if 'whitepaper' in file.lower() or file.endswith('.md'):
                    full_path = os.path.join(root, file)
                    whitepapers.append(full_path)
    except Exception as e:
        print(f"Error scanning whitepapers: {e}")
    return whitepapers

def main():
    try:
        workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        logs = get_git_log(15)
        papers = scan_whitepapers(workspace_dir)
        
        summary = {
            "timestamp": datetime.datetime.now().isoformat(),
            "git_logs": logs,
            "detected_documents": papers[:20]
        }
        
        output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, 'release_summary.json')
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=4)
            
        print(f"Successfully generated release summary at: {output_path}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
