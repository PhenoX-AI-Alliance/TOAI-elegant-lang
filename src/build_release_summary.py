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
            ['git', 'log', '-n', '10', '--pretty=format:%h - %an, %ar: %s'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except Exception as e:
        return f"Git log unavailable: {str(e)}"

def scan_workspace():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    white_papers = []
    try:
        for root, dirs, files in os.walk(workspace_dir):
            for file in files:
                if 'white' in file.lower() or 'paper' in file.lower() or file.endswith('.md'):
                    white_papers.append(os.path.join(root, file))
    except Exception as e:
        print(f"Error scanning workspace: {e}", file=sys.stderr)
    return white_papers

def main():
    try:
        print("Starting release summary generation...")
        git_history = get_git_log()
        papers = scan_workspace()
        
        summary_data = {
            "timestamp": datetime.datetime.now().isoformat(),
            "git_log": git_history,
            "detected_documents_count": len(papers),
            "documents_sample": papers[:5]
        }
        
        workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
        os.makedirs(output_dir, exist_ok=True)
        
        output_path = os.path.join(output_dir, 'release_summary.json')
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, ensure_ascii=False, indent=2)
            
        print(f"Release summary successfully built and saved to {output_path}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
