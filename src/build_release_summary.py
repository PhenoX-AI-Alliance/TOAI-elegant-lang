import sys
import os
import traceback
import subprocess
import datetime
import json

def get_git_log():
    try:
        result = subprocess.run(
            ['git', 'log', '-n', '10', '--oneline'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except Exception as e:
        return f"Git log retrieval failed: {str(e)}"

def scan_whitepaper():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    whitepaper_paths = [
        os.path.join(workspace, 'WHITE_PAPER.md'),
        os.path.join(workspace, 'CONSTITUTION.md')
    ]
    summary = {}
    for path in whitepaper_paths:
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    summary[os.path.basename(path)] = content[:500] + "..." if len(content) > 500 else content
            except Exception as e:
                summary[os.path.basename(path)] = f"Error reading file: {str(e)}"
        else:
            summary[os.path.basename(path)] = "File not found."
    return summary

def main():
    try:
        print("Starting Release Summary Build...")
        git_history = get_git_log()
        whitepaper_info = scan_whitepaper()
        
        release_summary = {
            "timestamp": datetime.datetime.now().isoformat(),
            "git_recent_commits": git_history.splitlines(),
            "whitepaper_snippets": whitepaper_info,
            "version": "1.0.0-gaia"
        }
        
        workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        output_file = os.path.join(workspace, 'TOAI_Generated', 'release_summary.json')
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(release_summary, f, ensure_ascii=False, indent=4)
            
        print(f"Release summary successfully built at: {output_file}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
