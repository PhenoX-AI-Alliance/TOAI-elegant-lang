import sys
import os
import subprocess
import json
from datetime import datetime

def get_git_log(max_count=10):
    try:
        result = subprocess.run(
            ['git', 'log', f'-n', str(max_count), '--pretty=format:%h - %an, %ar : %s'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Git log retrieval failed: {str(e)}"]

def scan_whitepapers():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    papers = []
    try:
        for root, dirs, files in os.walk(workspace):
            for file in files:
                if 'whitepaper' in file.lower() or file.endswith('.md'):
                    papers.append(os.path.join(root, file))
    except Exception as e:
        pass
    return papers

def main():
    print("Building release summary...")
    logs = get_git_log()
    papers = scan_whitepapers()
    
    summary = {
        "timestamp": datetime.utcnow().isoformat() + " Z",
        "recent_commits": logs,
        "related_documents_count": len(papers),
        "documents": papers[:10]
    }
    
    output_dir = os.path.join(os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/'), 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'release_summary.json')
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
        
    print(f"Release summary successfully written to {output_path}")

if __name__ == '__main__':
    main()
