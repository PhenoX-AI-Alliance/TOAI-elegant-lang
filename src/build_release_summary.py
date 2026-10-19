import sys
import os
import traceback
import time
import json
import subprocess
from datetime import datetime

def get_git_log():
    try:
        result = subprocess.run(
            ['git', 'log', '-n', '10', '--pretty=format:%h - %an: %s (%ad)'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
            timeout=10
        )
        return result.stdout.strip()
    except Exception as e:
        return f"Git log unavailable: {str(e)}"

def main():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    summary_dir = os.path.join(workspace, 'TOAI_Generated', 'releases')
    os.makedirs(summary_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = os.path.join(summary_dir, f'release_summary_{timestamp}.json')
    
    git_history = get_git_log()
    
    summary_data = {
        "version": "1.0.0",
        "timestamp": timestamp,
        "ecosystem": "Gaia Ecosystem - TOAI Elegant Lang",
        "git_log": git_history,
        "status": "stable",
        "message": "Altruistic monetization and sustainable architecture compiled successfully."
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(summary_data, f, ensure_ascii=False, indent=4)
        
    print(f"Release summary successfully built at: {output_file}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
