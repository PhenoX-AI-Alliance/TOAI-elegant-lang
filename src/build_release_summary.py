import sys
import os
import subprocess
from datetime import datetime

def get_git_log():
    try:
        log = subprocess.check_output(['git', 'log', '-n', '10', '--pretty=format:%h - %s (%an)'], encoding='utf-8')
        return log
    except Exception as e:
        return f"Error fetching git log: {e}"

def generate_summary():
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_data = get_git_log()
    
    summary = f"""# Release Summary
Generated at: {timestamp}

## Recent Changes
{log_data}

## Version Overview
- Current Branch: {subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], encoding='utf-8').strip()}
- Latest Commit: {subprocess.check_output(['git', 'rev-parse', 'HEAD'], encoding='utf-8').strip()[:7]}
"""
    with open('RELEASE_NOTES.md', 'w') as f:
        f.write(summary)
    print("Release summary generated successfully.")

if __name__ == "__main__":
    generate_summary()
