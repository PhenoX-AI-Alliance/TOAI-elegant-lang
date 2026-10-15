import sys
import os
import traceback
import time
import json
import subprocess

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
        return f"Git log not available: {str(e)}"

def main():
    try:
        workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        target_dir = os.path.join(workspace, 'TOAI-elegant-lang', 'src')
        os.makedirs(target_dir, exist_ok=True)
        
        log_data = get_git_log()
        
        summary = {
            "version": "1.0.0",
            "timestamp": time.time(),
            "git_history": log_data
        }
        
        output_path = os.path.join(target_dir, 'release_summary.json')
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
            
        print(f"Successfully generated release summary at {output_path}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
