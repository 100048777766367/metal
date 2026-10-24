# Ingest into GraphRAG
import json
with open('bodhi_knowledge_graph.jsonl') as f:
    print(f'Ingesting {len(f.readlines())} triplets...')
