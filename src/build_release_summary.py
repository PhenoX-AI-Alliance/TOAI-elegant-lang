import sys
import os
import traceback
import time
import json
import subprocess
import datetime

def get_git_log():
    try:
        result = subprocess.run(
            ['git', 'log', '-n', '10', '--oneline'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip().splitlines()
    except Exception as e:
        return [f"Git log retrieval failed: {str(e)}"]

def scan_documents():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    docs = []
    try:
        for root, dirs, files in os.walk(workspace_dir):
            for file in files:
                if file.endswith('.md') and ('whitepaper' in file.lower() or 'release' in file.lower() or 'summary' in file.lower()):
                    docs.append(os.path.join(root, file))
    except Exception as e:
        pass
    return docs

def main():
    try:
        workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
        os.makedirs(output_dir, exist_ok=True)
        
        git_commits = get_git_log()
        whitepapers = scan_documents()
        
        summary_data = {
            "timestamp": datetime.datetime.now().isoformat(),
            "recent_commits": git_commits,
            "relevant_documents": whitepapers,
            "status": "success",
            "message": "Release summary successfully generated with altruistic care."
        }
        
        output_path = os.path.join(output_dir, 'release_summary.json')
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, ensure_ascii=False, indent=2)
            
        print(f"Release summary successfully written to {output_path}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
