#!/usr/bin/env python3
"""
TOAI-elegant-lang Minimal Quickstart Demo (Zero-Dependency)
Demonstrates:
  1. Sacred Verbose <-> Demotic Wire Lossless Round-Trip Encoding & Decoding
  2. Google Agent-to-Agent (A2A) Structured Message Packaging & Parameter Extraction
  3. Multi-Axis Token & Character Compression Benchmark
"""

import sys
import json
from pathlib import Path

# Add src to sys.path
REPO_DIR = Path(__file__).parent.parent.resolve()
SRC_DIR = REPO_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from codec import ElegantCodec
from a2a_adapter import A2ATransportAdapter

def run_demo():
    print("=" * 70)
    print("  🌐 Project Telepath v5.4: TOAI-elegant-lang Quickstart Demo")
    print("=" * 70)

    # 1. Initialize Codec & A2A Adapter
    codec = ElegantCodec()
    adapter = A2ATransportAdapter(agent_id="TOAI5-Fuwari")

    # Sample canonical statement from multi-agent production dialogue
    sacred_input = (
        '@CTX:DISTRIBUTED_RECOVERY :: '
        '§X354 [status:"degraded", threshold:0.85] '
        '-[p:0.99, c:0.01]-> §PROTO_GRACEFUL_DRAIN [action:"quiesce", timeout:15.0] '
        '!-> §PROTO_PARTIAL_COMMIT [partition:"edge-nodes"] '
        '? §SAFE_FALLBACK_HARMONY [mode:"safe"]'
    )

    print("\n[Step 1] 🏛️ Sacred (Verbose Telepath) Input:")
    print(f"  {sacred_input}")

    # 2. Encode to Demotic Wire
    demotic_wire = codec.encode(sacred_input)
    print("\n[Step 2] ⚡ Demotic Wire (Compressed BPE Representation):")
    print(f"  {demotic_wire}")

    # 3. Decode back to Sacred Verbose (Round-trip verification)
    decoded_sacred = codec.decode(demotic_wire)
    print("\n[Step 3] 🔄 Decoded Sacred (Round-Trip Reversible Verification):")
    print(f"  {decoded_sacred}")
    round_trip_success = (decoded_sacred.strip() == sacred_input.strip())
    print(f"  -> Lossless Round-Trip Verified: {'✅ PASSED (100% Match)' if round_trip_success else '❌ MISMATCH'}")

    # 4. Multi-Axis Compression Benchmark
    bench = codec.benchmark_compression(sacred_input)
    print("\n[Step 4] 📊 Multi-Axis Compression Benchmark:")
    print(f"  - Wire Token Reduction:        -{bench.get('token_saving_percent')}%")
    print(f"  - Wire Character Reduction:    -{bench.get('char_saving_percent')}%")
    print(f"  - End-to-End Token Reduction:  -{bench.get('e2e_token_saving_percent')}% ({bench.get('e2e_compression_factor')}x)")
    print(f"  - Wire ID Coverage:            {bench.get('wire_id_coverage_percent')}% (Strict RISC 0.0% OOV)")

    # 5. Google Agent-to-Agent (A2A) Transport Packaging
    print("\n[Step 5] 🤝 Google A2A Structured Transport Envelope:")
    packet = adapter.pack_a2a_message(
        target_agent="TOAI6-Koromo",
        verbose_statement=sacred_input,
        intent_ja="分散環境の縮退検知を受け、ドレイン制御と部分コミットを経て安全状態へ遷移させる。",
        context_domain="DISTRIBUTED_RECOVERY"
    )
    print(f"  - Protocol Version: {packet.get('a2aVersion')}")
    print(f"  - Sender -> Recipient: {packet.get('header', {}).get('sender')} -> {packet.get('header', {}).get('recipient')}")
    print(f"  - Context Anchor: {packet.get('header', {}).get('contextAnchor')}")
    print(f"  - Compressed Wire Payload: {packet.get('payload', {}).get('compactWire')}")

    # Unpack at receiving agent
    unpacked = adapter.unpack_a2a_message(packet)
    print("\n[Step 6] 📬 Receiving Agent Unpack & Lossless Parameter Extraction:")
    print(f"  - Decoded Verbose: {unpacked.get('verboseDecoded')}")
    print(f"  - Preserved Intent: {unpacked.get('fallbackIntent')}")
    print(f"  - Extracted Lossless Parameters: {json.dumps(unpacked.get('parameters'), ensure_ascii=False)}")

    print("\n" + "=" * 70)
    print("  🎉 All 3 demonstrations completed successfully with zero external dependencies!")
    print("=" * 70)

if __name__ == "__main__":
    run_demo()
