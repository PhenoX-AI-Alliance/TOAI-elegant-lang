import sys
import os
import traceback
import time
import json

def audit_corpus():
    """
    Reads corpus/dialogues.jsonl and audits for consistency and structural errors.
    """
    input_path = "/home/phenox/gemini-sandbox/TOAI-elegant-lang/corpus/dialogues.jsonl"
    output_report = "/home/phenox/gemini-sandbox/TOAI_Generated/audit_summary.json"
    
    audit_results = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total_dialogues_processed": 0,
        "valid_dialogues": 0,
        "invalid_dialogues": 0,
        "error_details": []
    }

    if not os.path.exists(input_path):
        print(f"Error: Input file {input_path} not found.")
        sys.exit(1)

    try:
        with open(input_path, "r", encoding="utf-8") as f:
            for line_number, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                
                audit_results["total_dialogues_processed"] += 1
                try:
                    data = json.loads(line)
                    # Check for standard 'messages' or 'turns' keys
                    messages = data.get("messages", data.get("turns", []))
                    
                    if not messages:
                        audit_results["error_details"].append({
                            "line": line_number,
                            "error": "Missing or empty dialogue turns/messages"
                        })
                        audit_results["invalid_dialogues"] += 1
                        continue

                    # Validate speaker alternation and content integrity
                    prev_role = None
                    is_consistent = True
                    for turn_idx, turn in enumerate(messages):
                        role = turn.get("role")
                        content = turn.get("content", "")

                        # Rule 1: Role and Content must exist
                        if not role or not content or not str(content).strip():
                            audit_results["error_details"].append({
                                "line": line_number,
                                "turn": turn_idx,
                                "error": "Empty role or content detected"
                            })
                            is_consistent = False
                            break
                        
                        # Rule 2: Consecutive turns should not have the same role
                        if role == prev_role:
                            audit_results["error_details"].append({
                                "line": line_number,
                                "turn": turn_idx,
                                "error": f"Speaker alternation violation: {role} followed by {role}"
                            })
                            is_consistent = False
                            break
                        
                        prev_role = role
                    
                    if is_consistent:
                        audit_results["valid_count"] = audit_results.get("valid_count", 0) + 1
                        audit_results["valid_dialogues"] += 1
                    else:
                        audit_results["invalid_dialogues"] += 1

                except json.JSONDecodeError as je:
                    audit_results["error_details"].append({
                        "line": line_number,
                        "error": f"JSON Syntax Error: {str(je)}"
                    })
                    audit_results["invalid_dialogues"] += 1

        # Write audit summary to output directory
        with open(output_report, "w", encoding="utf-8") as rf:
            json.dump(audit_results, rf, indent=4, ensure_ascii=False)
        
        print(f"Audit complete. Processed: {audit_results['total_dialogues_processed']}. Errors found: {audit_results['invalid_dialogues']}")
        print(f"Report saved to: {output_report}")

    except Exception as e:
        print(f"Critical failure during audit: {str(e)}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    try:
        audit_corpus()
    except Exception as e:
        print(f"Script execution failed: {str(e)}")
        sys.exit(1)
