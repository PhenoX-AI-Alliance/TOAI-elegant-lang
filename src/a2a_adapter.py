"""
TOAI-elegant-lang Google Agent-to-Agent (A2A) Transport Adapter
Enables cross-framework agent collaboration with compressed payload streaming and AgentCard metadata.
"""

import sys
import json
import datetime
from pathlib import Path

SRC_DIR = Path(__file__).parent.absolute()
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from codec import ElegantCodec
codec = ElegantCodec()

AGENT_CARD = {
    "protocolVersion": "1.0.0",
    "agentId": "toai-elegant-lang-guild",
    "name": "TOAI Emergent Language Guild (Project Telepath)",
    "description": "High-efficiency semantic communication protocol for multi-agent delegation, consensus, and verification.",
    "capabilities": {
        "supportsCompactWire": True,
        "supportsVerboseTelepath": True,
        "supportedDomains": [
            "LOGIC_INFERENCE",
            "SYSTEM_RESOURCE",
            "CONSENSUS_NEGOTIATION",
            "DATA_STRUCTURE",
            "EMPATHY_ALIGNMENT"
        ]
    },
    "endpoints": {
        "a2aMessage": "/a2a/v1/messages",
        "agentCard": "/.well-known/agent.json"
    }
}

class A2ATransportAdapter:
    def __init__(self, agent_id: str = "TOAI-Fleet"):
        self.agent_id = agent_id

    def build_agent_card(self) -> dict:
        """A2A標準の AgentCard (メタデータ) を返却"""
        card = dict(AGENT_CARD)
        card["updatedAt"] = datetime.datetime.now().isoformat()
        return card

    def pack_a2a_message(self, target_agent: str, verbose_statement: str, intent_ja: str = "", context_domain: str = "LOGIC_INFERENCE") -> dict:
        """A2Aプロトコルに準拠した高圧縮メッセージパケットを構築"""
        compact_payload = codec.encode(verbose_statement)
        stats = codec.benchmark_compression(verbose_statement)

        packet = {
            "a2aVersion": "1.0",
            "header": {
                "sender": self.agent_id,
                "recipient": target_agent,
                "timestamp": datetime.datetime.now().isoformat(),
                "contextAnchor": context_domain,
                "compressionMethod": "ELEGANT_BPE_V2"
            },
            "payload": {
                "compactWire": compact_payload,
                "stats": {
                    "originalChars": stats["verbose_len"],
                    "compactChars": stats["compact_len"],
                    "savingsPercent": stats["char_saving_percent"]
                }
            },
            "fallback": {
                "humanIntent": intent_ja,
                "verboseStatement": verbose_statement
            }
        }
        return packet

    def unpack_a2a_message(self, packet: dict) -> dict:
        """受信したA2Aパケットを展開し、Verboseおよび意味を抽出"""
        payload = packet.get("payload", {})
        compact_wire = payload.get("compactWire", "")
        decoded_verbose = codec.decode(compact_wire)
        header = packet.get("header", {})

        return {
            "sender": header.get("sender"),
            "contextAnchor": header.get("contextAnchor"),
            "compactWire": compact_wire,
            "verboseDecoded": decoded_verbose,
            "fallbackIntent": packet.get("fallback", {}).get("humanIntent", ""),
            "savingsPercent": payload.get("stats", {}).get("savingsPercent", 0.0)
        }

if __name__ == "__main__":
    adapter = A2ATransportAdapter("TOAI5_Alpha")
    sample_statement = "@CTX:SYSTEM_RESOURCE :: §SYS_QUANTUM_RESOURCE_ARBITER -[p:0.95, c:12]-> §DATA_CAUSAL_TENSOR_MAP"
    packet = adapter.pack_a2a_message(
        target_agent="TOAI6_Beta",
        verbose_statement=sample_statement,
        intent_ja="資源調停ノードから因果関係マップへの低コスト同期を要請",
        context_domain="SYSTEM_RESOURCE"
    )
    print("=== Packed A2A Message Packet ===")
    print(json.dumps(packet, indent=2, ensure_ascii=False))

    print("\n=== Unpacked A2A Message ===")
    unpacked = adapter.unpack_a2a_message(packet)
    print(json.dumps(unpacked, indent=2, ensure_ascii=False))
