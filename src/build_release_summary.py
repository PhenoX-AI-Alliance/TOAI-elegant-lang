import sys
import os
import traceback
import time
import json
import subprocess
import datetime

def get_git_log():
    try:
        repo_path = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        TOAI_elegant_dir = os.path.join(repo_path, 'TOAI-elegant-lang')
        if not os.path.exists(os.path.join(TOAI_elegant_dir, '.git')):
            return "Git repository not found in target path."
        
        result = subprocess.run(
            ['git', 'log', '-n', '10', '--oneline'],
            cwd=TOAI_elegant_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout
    except Exception as e:
        return f"Could not retrieve git log: {str(e)}"

def scan_whitepaper():
    try:
        repo_path = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        TOAI_elegant_dir = os.path.join(repo_path, 'TOAI-elegant-lang')
        
        files_found = []
        for root, dirs, files in os.walk(TOAI_elegant_dir):
            for file in files:
                if 'whitepaper' in file.lower() or 'readme' in file.lower() or file.endswith('.md'):
                    files_found.append(os.path.join(root, file))
        
        summary = "Scanned Markdown/Whitepaper Files:\n"
        for f in files_found[:5]:
            summary += f"- {os.path.relpath(f, TOAI_elegant_dir)}\n"
        return summary
    except Exception as e:
        return f"Could not scan whitepaper: {str(e)}"

def main():
    try:
        workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        output_dir = os.path.join(workspace, 'TOAI_Generated')
        os.makedirs(output_dir, exist_ok=True)
        
        git_history = get_git_log()
        whitepaper_info = scan_whitepaper()
        
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        release_summary = f"""# TOAI Elegant Lang Release Summary
Generated at: {timestamp}

## Recent Changes (Git Log)
{git_history}

## Documentation & Whitepaper Status
{whitepaper_info}
"""
        
        output_file_path = os.path.join(output_dir, 'release_summary.md')
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write(release_summary)
            
        print(f"Successfully generated release summary at: {output_file_path}")
        
    except Exception as e:
        print(f"Error in release summary builder: {str(e)}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
