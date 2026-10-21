#!/usr/bin/env python3
import sys
import os
import subprocess
import json
import datetime

def get_git_log(max_count=10):
    try:
        result = subprocess.run(
            ['git', 'log', f'-n {max_count}', '--pretty=format:%h - %an, %ar : %s'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.strip().split('\n')
    except Exception as e:
        return [f"Git log unavailable: {str(e)}"]

def scan_whitepaper():
    whitepaper_candidates = [
        "WHITEPAPER.md",
        "docs/WHITEPAPER.md",
        "CONSTITUTION.md"
    ]
    found_content = ""
    for path in whitepaper_candidates:
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    found_content = f.read()[:1000]
                break
            except Exception:
                pass
    return found_content

def main():
    print("Generating release summary for TOAI-elegant-lang...")
    git_history = get_git_log(15)
    whitepaper_snippet = scan_whitepaper()
    
    summary = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "git_logs": git_history,
        "whitepaper_overview": whitepaper_snippet
    }
    
    output_file = "release_summary.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    print(f"Successfully generated {output_file}")

if __name__ == "__main__":
    main()
