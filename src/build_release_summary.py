import sys
import os
import subprocess
import json
import datetime

def get_git_log(max_count=10):
    try:
        cmd = ['git', 'log', f'-n', str(max_count), '--pretty=format:%h - %an, %ar : %s']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True, cwd=os.path.dirname(os.path.abspath(__file__)))
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Git log retrieval failed: {str(e)}"]

def scan_whitepapers(base_dir):
    whitepapers = []
    try:
        for root, dirs, files in os.walk(base_dir):
            for file in files:
                if 'whitepaper' in file.lower() or file.endswith('.md'):
                    whitepapers.append(os.path.join(root, file))
    except Exception as e:
        pass
    return whitepapers

def main():
    print("Generating Release Summary...")
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    logs = get_git_log(15)
    
    summary = {
        "timestamp": datetime.datetime.now().isoformat(),
        "git_history": logs,
        "version": "1.0.0-gaia"
    }
    
    output_path = os.path.join(workspace_dir, 'TOAI_Generated', 'release_summary.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
        
    print(f"Release summary successfully generated at: {output_path}")

if __name__ == '__main__':
    main()
