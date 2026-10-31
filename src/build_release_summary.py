import sys
import os
import traceback
import time
import json
import subprocess
from datetime import datetime

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

def scan_whitepapers(workspace_dir):
    whitepaper_dir = os.path.join(workspace_dir, 'TOAI-elegant-lang')
    papers = []
    if os.path.exists(whitepaper_dir):
        for root, dirs, files in os.walk(whitepaper_dir):
            for file in files:
                if file.endswith('.md') or file.endswith('.txt'):
                    papers.append(os.path.join(root, file))
    return papers

def main():
    try:
        workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
        os.makedirs(output_dir, exist_ok=True)
        
        logs = get_git_logs()
        papers = scan_whitepapers(workspace_dir)
        
        summary = {
            "timestamp": datetime.now().isoformat(),
            "git_logs": logs,
            "whitepapers": papers,
            "version": "1.0.0",
            "status": "release_summary_generated"
        }
        
        output_path = os.path.join(output_dir, 'release_summary.json')
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
            
        print(f"Successfully generated release summary at: {output_path}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
