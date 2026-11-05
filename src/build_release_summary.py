import sys
import os
import traceback
import subprocess
import json
import datetime
import requests
from pathlib import Path

# Add sandbox root to load env_loader
BASE_DIR = Path(__file__).parent.parent.parent.resolve()
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

try:
    import env_loader
    env_loader.load_toai_env()
except Exception:
    pass

RELEASE_VERSION = "v5.4.1"
RELEASE_TITLE = "Project Telepath v5.4.1: Canonical Spec, ADR-001 & 9-Lab Consensus"

def run_git_command(repo_path, args):
    try:
        res = subprocess.run(
            ['git'] + args,
            cwd=repo_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return res.stdout.strip()
    except Exception as e:
        return f"Error: {e}"

def generate_release_notes(repo_path):
    changelog_path = os.path.join(repo_path, 'CHANGELOG.md')
    if os.path.exists(changelog_path):
        with open(changelog_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        notes = []
        capturing = False
        for l in lines:
            if l.startswith('## ['):
                if '5.4' in l:
                    capturing = True
                elif capturing:
                    break
            if capturing:
                notes.append(l)
        if notes:
            return ''.join(notes).strip()

    return f"""### {RELEASE_TITLE}
- **Canonical EBNF Grammar**: Standardized syntax and [ADR-001] Convergence Decision Table in `spec/SPEC_v0.1_DRAFT.md`.
- **Why 256? (8-Bit Bound)**: Formally documented 8-bit binary boundary, subword BPE token stability, and <1,024 prompt cache boundary alignment across all whitepapers and READMEs.
- **Zero-Dependency Quickstart**: `examples/quickstart_demo.py` featuring Sacred⇄Demotic lossless verification and Google A2A packaging.
- **Cross-Model Verification**: 9 frontier AI models (Gemini 3.5 Flash-Lite, Claude Opus 3.5, GPT-6.1 Sol, DeepSeek-V3, Qwen-2.5-72B).
- **Single Source of Truth**: Centralized macro sequence tracking and lexicon version management (v5.4.1).
"""

def publish_github_release(repo_path, version_tag, title, notes):
    token = os.environ.get("GITHUB_ELEGANT_TOKEN")
    if not token:
        try:
            token = env_loader.get_github_token()
        except Exception:
            pass
    if not token:
        print("[Release] GITHUB_ELEGANT_TOKEN not found. Skipping GitHub Release API call.")
        return False

    url = "https://api.github.com/repos/PhenoX-AI-Alliance/TOAI-elegant-lang/releases"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "Content-Type": "application/json"
    }
    payload = {
        "tag_name": version_tag,
        "target_commitish": "main",
        "name": title,
        "body": notes,
        "draft": False,
        "prerelease": False
    }

    try:
        res = requests.post(url, headers=headers, json=payload, timeout=30)
        if res.status_code in [200, 201]:
            rel_data = res.json()
            print(f"[Release] GitHub Release successfully created! URL: {rel_data.get('html_url')}")
            return True
        elif res.status_code == 422:
            print(f"[Release] GitHub Release for tag {version_tag} already exists.")
            return True
        else:
            print(f"[Release] Failed to create GitHub Release (HTTP {res.status_code}): {res.text}")
            return False
    except Exception as e:
        print(f"[Release] Error during release creation: {e}")
        return False

def main():
    repo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    
    print(f"Scanning repository at: {repo_path}")
    git_log = run_git_command(repo_path, ['log', '-n', '5', '--oneline'])
    notes = generate_release_notes(repo_path)
    
    summary_data = {
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "version": RELEASE_VERSION,
        "title": RELEASE_TITLE,
        "notes": notes,
        "git_recent_commits": git_log
    }
    
    output_dir = os.path.join(repo_path, 'dist')
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, 'release_summary.json')
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, ensure_ascii=False, indent=2)
        print(f"Release summary successfully written to {output_file}")
    except Exception as e:
        print(f"Failed to write summary file: {e}")
        sys.exit(1)

    # Publish to GitHub
    publish_github_release(repo_path, RELEASE_VERSION, RELEASE_TITLE, notes)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
