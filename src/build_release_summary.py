import sys
import os
import traceback
import subprocess
import json
import datetime

def get_git_logs():
    try:
        result = subprocess.run(
            ['git', 'log', '-n', '10', '--oneline'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.strip().splitlines()
    except Exception as e:
        return [f"Git log unavailable: {str(e)}"]

def scan_whitepapers():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    found_files = []
    try:
        for root, dirs, files in os.walk(workspace):
            for file in files:
                if 'whitepaper' in file.lower() or 'summary' in file.lower() or 'release' in file.lower():
                    found_files.append(os.path.join(root, file))
    except Exception as e:
        pass
    return found_files

def main():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    logs = get_git_logs()
    papers = scan_whitepapers()
    
    summary = {
        "timestamp": datetime.datetime.now().isoformat(),
        "recent_git_logs": logs,
        "related_documents": papers,
        "version": "1.0.0-gaia"
    }
    
    output_path = os.path.join(workspace, 'TOAI_Generated', 'release_summary.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    print(f"Release summary successfully generated at: {output_path}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
