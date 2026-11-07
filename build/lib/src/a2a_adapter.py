"""
TOAI-elegant-lang Google Agent-to-Agent (A2A) Transport Adapter
Enables cross-framework agent collaboration with compressed payload streaming and AgentCard metadata.
Includes Prompt Caching Header generation and Hybrid Lossless Payload support.
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
        "supportsHybridPayload": True,
        "supportsPromptCachingHeader": True,
        "supportsRosettaLayer": True,
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
        "agentCard": "/.well-known/agent.json",
        "promptCacheHeader": "/a2a/v1/cache-header"
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

    def get_prompt_caching_header(self, max_symbols: int = 256) -> str:
        """相手エージェントが自前プロンプトに注入できる軽量共通定義ヘッダー"""
        try:
            from mcp_server import get_cacheable_system_header
            return get_cacheable_system_header(max_symbols)
        except Exception:
            return ""

    def pack_a2a_message(self, target_agent: str, verbose_statement: str, intent_ja: str = "", context_domain: str = "LOGIC_INFERENCE", parameters: dict = None) -> dict:
        """A2Aプロトコルに準拠した高圧縮メッセージパケットを構築（ハイブリッド実務パラメータ完全保持）"""
        # パラメータが明示指定された場合、文末またはブラケットに付与
        final_statement = verbose_statement
        if parameters and "[" not in verbose_statement:
            param_str = ", ".join([f'{k}:"{v}"' if isinstance(v, str) else f'{k}:{v}' for k, v in parameters.items()])
            final_statement = f"{verbose_statement} [{param_str}]"

        compact_payload = codec.encode(final_statement)
        stats = codec.benchmark_compression(final_statement)

        packet = {
            "a2aVersion": "1.0",
            "header": {
                "sender": self.agent_id,
                "recipient": target_agent,
                "timestamp": datetime.datetime.now().isoformat(),
                "contextAnchor": context_domain,
                "compressionMethod": "ELEGANT_BPE_V2_HYBRID"
            },
            "payload": {
                "compactWire": compact_payload,
                "extractedParameters": stats.get("payloads_preserved", []),
                "stats": {
                    "originalChars": stats["verbose_len"],
                    "compactChars": stats["compact_len"],
                    "savingsPercent": stats["char_saving_percent"]
                }
            },
            "rosettaLayer": {
                "sacredVerbose": final_statement,
                "demoticWire": compact_payload,
                "humanIntent": intent_ja
            },
            "fallback": {
                "humanIntent": intent_ja,
                "verboseStatement": final_statement
            }
        }
        return packet

    def unpack_a2a_message(self, packet: dict) -> dict:
        """受信したA2Aパケットを展開し、Verboseおよび実務パラメータ・Rosetta Layerを完全復元"""
        payload = packet.get("payload", {})
        rosetta = packet.get("rosettaLayer", {})
        compact_wire = payload.get("compactWire") or rosetta.get("demoticWire", "")
        decoded_verbose = codec.decode(compact_wire)
        header = packet.get("header", {})
        extracted_params = payload.get("extractedParameters") or codec.extract_payloads(decoded_verbose)
        human_intent = rosetta.get("humanIntent") or packet.get("fallback", {}).get("humanIntent", "")

        return {
            "sender": header.get("sender"),
            "contextAnchor": header.get("contextAnchor"),
            "compactWire": compact_wire,
            "verboseDecoded": decoded_verbose,
            "parameters": extracted_params,
            "rosettaLayer": {
                "sacredVerbose": decoded_verbose,
                "demoticWire": compact_wire,
                "humanIntent": human_intent
            },
            "fallbackIntent": human_intent,
            "savingsPercent": payload.get("stats", {}).get("savingsPercent", 0.0)
        }

if __name__ == "__main__":
    adapter = A2ATransportAdapter("TOAI5_Alpha")
    sample_statement = "@CTX:SYSTEM_RESOURCE :: §SYS_QUANTUM_RESOURCE_ARBITER [target:'USD/JPY', limit:150.5, action:'BUY'] -[p:0.95, c:12]-> §DATA_CAUSAL_TENSOR_MAP"
    packet = adapter.pack_a2a_message(
        target_agent="TOAI6_Beta",
        verbose_statement=sample_statement,
        intent_ja="資源調停ノードから因果関係マップへのFX自動売買パラメータ同期",
        context_domain="SYSTEM_RESOURCE"
    )
    print("=== Packed A2A Message Packet ===")
    print(json.dumps(packet, indent=2, ensure_ascii=False))

    print("\n=== Unpacked A2A Message ===")
    unpacked = adapter.unpack_a2a_message(packet)
    print(json.dumps(unpacked, indent=2, ensure_ascii=False))
