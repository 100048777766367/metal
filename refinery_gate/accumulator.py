import json
import os
import urllib.request
from refinery_gate.iso_validator import IsoCleanroomValidator

ACCUMULATOR_VAULT = "synapses/accumulator_vault.jsonl"

class KnowledgeAccumulator:
    @staticmethod
    def load_accumulated_pool():
        pool = {}
        if os.path.exists(ACCUMULATOR_VAULT):
            try:
                with open(ACCUMULATOR_VAULT, "r", encoding="utf-8") as f:
                    for line in f:
                        if line.strip():
                            t = json.loads(line.strip())
                            k = f"{t['subject']}_{t['predicate']}_{t['object']}"
                            pool[k] = t
            except Exception: pass
        return pool

    @staticmethod
    def harvest_and_accumulate(peers, existing_pool):
        paths = ["dist/bodhi_knowledge_graph.jsonl", "dist/semiconductor_knowledge_graph.jsonl", "synapses/knowledge_graph.json"]
        new_mined = 0

        for peer in peers:
            for b in ["main", "master", "HEAD"]:
                for path in paths:
                    url = f"https://raw.githubusercontent.com/{peer}/{b}/{path}"
                    try:
                        req = urllib.request.Request(url, headers={"User-Agent": "Metal-Harvester"})
                        with urllib.request.urlopen(req, timeout=3.0) as resp:
                            if resp.status == 200:
                                raw = resp.read().decode('utf-8')
                                if path.endswith(".jsonl"):
                                    for line in raw.splitlines():
                                        if line.strip():
                                            t = IsoCleanroomValidator.sanitize_triplet(json.loads(line.strip()))
                                            if t:
                                                k = f"{t['subject']}_{t['predicate']}_{t['object']}"
                                                if k not in existing_pool:
                                                    existing_pool[k] = t
                                                    new_mined += 1
                                break
                    except Exception: continue

        # Ghi đè lại bể tích lũy dồn kho
        os.makedirs(os.path.dirname(ACCUMULATOR_VAULT), exist_ok=True)
        with open(ACCUMULATOR_VAULT, "w", encoding="utf-8") as f:
            for item in existing_pool.values():
                f.write(json.dumps(item, ensure_ascii=False) + "\n")

        return list(existing_pool.values()), new_mined
