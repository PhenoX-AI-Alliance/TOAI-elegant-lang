import sys
import os
import traceback
import subprocess
import json
import datetime

def get_git_log():
    try:
        result = subprocess.run(
            ['git', 'log', '-n', '10', '--oneline'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except Exception as e:
        return f"Git log retrieval failed: {str(e)}"

def scan_whitepaper(workspace_dir):
    candidates = ['WHITE_PAPER.md', 'README.md', 'CONSTITUTION.md']
    snippet = "No whitepaper found."
    for name in candidates:
        path = os.path.join(workspace_dir, name)
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    snippet = content[:1000]
                    break
            except Exception:
                pass
    return snippet

def main():
    try:
        workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        git_history = get_git_log()
        whitepaper_snippet = scan_whitepaper(workspace)
        
        now = datetime.datetime.now().isoformat()
        
        summary = f"""# TOAI Release Summary
Generated at: {now}

## Recent Git Changes
{git_history}

## Whitepaper / Core Document Snapshot
{whitepaper_snippet}
"""
        
        output_path = os.path.join(workspace, 'TOAI_Generated', 'release_summary.md')
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(summary)
            
        print(f"Successfully generated release summary at: {output_path}")
        
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
