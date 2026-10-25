import sys
import os
import subprocess
import datetime
import json

def get_git_log(max_count=10):
    try:
        cmd = ['git', 'log', f'-n {max_count}', '--pretty=format:%h - %an: %s (%ad)']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=10)
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
        pass
    return whitepapers

def main():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    print(f"Scanning workspace: {workspace_dir}")
    
    logs = get_git_log()
    papers = scan_whitepapers(workspace_dir)
    
    summary = {
        "timestamp": datetime.datetime.now().isoformat(),
        "git_logs": logs,
        "whitepapers_found": len(papers),
        "whitepaper_paths": papers[:5]
    }
    
    output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    out_file = os.path.join(output_dir, 'release_summary.json')
    
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
        
    print(f"Release summary successfully generated at {out_file}")

if __name__ == '__main__':
    main()\n