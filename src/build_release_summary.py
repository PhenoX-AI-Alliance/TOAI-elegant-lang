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
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip().split('\n')
    except Exception as e:
        print(f"Warning: Could not fetch git log: {e}")
        return []

def scan_whitepaper():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    whitepaper_path = os.path.join(workspace_dir, 'TOAI-elegant-lang', 'docs', 'whitepaper.md')
    if os.path.exists(whitepaper_path):
        try:
            with open(whitepaper_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
                return lines[:20]
        except Exception as e:
            print(f"Warning: Could not read whitepaper: {e}")
    return ["Whitepaper not found or unreadable."]

def main():
    print("Starting release summary generation...")
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
    os.makedirs(output_dir, exist_ok=True)
    
    git_logs = get_git_log()
    whitepaper_summary = scan_whitepaper()
    
    release_data = {
        "timestamp": datetime.datetime.now().isoformat(),
        "version": "1.0.0",
        "recent_commits": git_logs,
        "whitepaper_excerpt": whitepaper_summary
    }
    
    output_file = os.path.join(output_dir, 'release_summary.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(release_data, f, ensure_ascii=False, indent=2)
        
    print(f"Successfully generated release summary at: {output_file}")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
