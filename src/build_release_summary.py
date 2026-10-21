import sys
import os
import traceback
import subprocess
import datetime
import json

def get_git_log(max_count=20):
    try:
        cmd = ['git', 'log', f'-n', str(max_count), '--pretty=format:%h - %an, %ar : %s']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True, cwd=os.getcwd())
        return result.stdout.splitlines()
    except Exception as e:
        return [f"Git log retrieval failed: {e}"]

def scan_whitepapers():
    papers = []
    search_dirs = ['.', 'docs', 'src', 'TOAI_Generated']
    for d in search_dirs:
        if os.path.exists(d) and os.path.isdir(d):
            for root, dirs, files in os.walk(d):
                for file in files:
                    if 'whitepaper' in file.lower() or 'release' in file.lower() or file.endswith('.md'):
                        papers.append(os.path.join(root, file))
    return papers

def build_summary():
    print("Building release summary for TOAI-elegant-lang...")
    git_commits = get_git_log()
    whitepapers = scan_whitepapers()
    
    summary = {
        "timestamp": datetime.datetime.now().isoformat(),
        "recent_commits": git_commits,
        "related_documents": whitepapers
    }
    
    output_file = os.path.abspath("release_summary.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
        
    print(f"Release summary successfully generated at: {output_file}")

if __name__ == '__main__':
    try:
        build_summary()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
