import os
import sys
import subprocess
import json
import datetime
import traceback

def get_git_log(max_count=20):
    try:
        cmd = ["git", "log", f"-n {max_count}", "--pretty=format:%h - %an, %ar : %s"]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True, encoding="utf-8")
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Git log unavailable: {str(e)}"]

def scan_whitepapers(workspace_dir):
    whitepaper_files = []
    try:
        for root, dirs, files in os.walk(workspace_dir):
            for file in files:
                if "whitepaper" in file.lower() or "summary" in file.lower() or file.endswith(".md"):
                    whitepaper_files.append(os.path.join(root, file))
    except Exception as e:
        pass
    return whitepaper_files

def main():
    try:
        workspace_dir = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
        output_dir = os.path.join(workspace_dir, 'TOAI_Generated')
        os.makedirs(output_dir, exist_ok=True)
        
        git_logs = get_git_log()
        whitepapers = scan_whitepapers(workspace_dir)
        
        summary_data = {
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "git_recent_commits": git_logs,
            "discovered_documents": whitepapers[:50]
        }
        
        output_file = os.path.join(output_dir, 'release_summary.json')
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, ensure_ascii=False, indent=2)
            
        print(f"Release summary successfully built at: {output_file}")
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
