import sys
import os
import traceback
import subprocess
import json
import datetime

def get_git_log():
    try:
        cmd = ['git', 'log', '-n', '10', '--pretty=format:%h - %an, %ar : %s']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True, encoding='utf-8')
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Git log unavailable: {str(e)}"]

def scan_workspace():
    workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    summary_data = {
        "timestamp": datetime.datetime.now().isoformat(),
        "git_logs": get_git_log(),
        "whitepapers": []
    }
    
    try:
        for root, dirs, files in os.walk(workspace_dir):
            for file in files:
                if "whitepaper" in file.lower() or file.endswith(".md"):
                    full_path = os.path.join(root, file)
                    summary_data["whitepapers"].append({
                        "path": full_path,
                        "size": os.path.getsize(full_path)
                    })
    except Exception as e:
        summary_data["scan_error"] = str(e)
        
    return summary_data

def main():
    try:
        workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
        os.makedirs(output_dir, exist_ok=True)
        
        summary = scan_workspace()
        
        output_path = os.path.join(output_dir, 'release_summary.json')
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
            
        print(f"Release summary successfully built at: {output_path}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()\n