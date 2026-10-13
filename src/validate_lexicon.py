import sys
import os
import json

def validate_lexicon():
    workspace = os.environ.get('TOAI_WORKSPACE_DIR', '/home/phenox/gemini-sandbox/')
    data_path = os.path.join(workspace, 'TOAI-elegant-lang', 'data', 'core_lexicon.json')
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Required file not found: {data_path}")
    
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    if not isinstance(data, list):
        raise ValueError("Lexicon data must be a list of objects.")
        
    required_fields = ['symbol', 'definition', 'japanese']
    for idx, item in enumerate(data):
        for field in required_fields:
            if field not in item:
                raise KeyError(f"Missing required field '{field}' at index {idx}")
                
    print("Lexicon validation successful!")

if __name__ == '__main__':
    try:
        validate_lexicon()
    except Exception as e:
        print(f"Validation failed: {e}", file=sys.stderr)
        sys.exit(1)
