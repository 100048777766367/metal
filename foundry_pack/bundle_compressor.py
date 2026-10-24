import os
import json
import zipfile
from foundry_pack.cypher_builder import CypherScriptBuilder

class CommercialBundleCompressor:
    @staticmethod
    def pack_if_threshold_met(triplets, threshold=10000, epoch=1):
        total_count = len(triplets)
        if total_count < threshold:
            print(f"⏳ [CHƯA ĐỦ ĐIỀU KIỆN 10K]: Hiện có {total_count}/{threshold} bản ghi ({round(total_count/threshold*100, 1)}%). Chưa đóng gói!")
            return None

        print(f"🎉 [ĐÃ ĐẠT NGƯỠNG QUỐC TẾ]: {total_count} >= {threshold}! KÍCH HOẠT ĐÚC THÀNH PHẨM ZIP...")
        os.makedirs("dist", exist_ok=True)

        # 1. Xuất file .jsonl và .csv
        jl = "dist/bodhi_knowledge_graph.jsonl"
        with open(jl, "w", encoding="utf-8") as f:
            for t in triplets: f.write(json.dumps(t, ensure_ascii=False) + "\n")

        csv_file = "dist/bodhi_knowledge_graph.csv"
        with open(csv_file, "w", encoding="utf-8") as f:
            f.write("subject,predicate,object,confidence\n")
            for t in triplets:
                s = t["subject"].replace('"', '""')
                p = t["predicate"].replace('"', '""')
                o = t["object"].replace('"', '""')
                f.write(f'"{s}","{p}","{o}",{t["confidence"]}\n')

        # 2. Xuất file .cypher (Neo4j)
        cypher_file = "dist/neo4j_import.cypher"
        with open(cypher_file, "w", encoding="utf-8") as f:
            f.write(CypherScriptBuilder.build_script(triplets))

        # 3. Tạo tài liệu đi kèm
        dict_file = "dist/DATA_DICTIONARY.md"
        with open(dict_file, "w", encoding="utf-8") as f:
            f.write("# 📖 BODHI METAL DATA DICTIONARY\n- subject: Head Entity\n- predicate: Relation\n- object: Tail Entity\n- confidence: Integrity Score\n")

        lic_file = "dist/LICENSE.txt"
        with open(lic_file, "w", encoding="utf-8") as f:
            f.write("COMMERCIAL ROYALTY-FREE DATASET LICENSE (V1.0)\nPermitted for unlimited commercial AI training & GraphRAG usage.\n")

        demo_file = "dist/quickstart_llamaindex.py"
        with open(demo_file, "w", encoding="utf-8") as f:
            f.write("# Ingest into GraphRAG\nimport json\nwith open('bodhi_knowledge_graph.jsonl') as f:\n    print(f'Ingesting {len(f.readlines())} triplets...')\n")

        # 4. Nén toàn bộ thành chiếc hộp ZIP thương mại hoàn hảo
        zip_path = f"dist/Bodhi_Metal_GraphRAG_{threshold//1000}K_Commercial.zip"
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for item in [jl, csv_file, cypher_file, dict_file, lic_file, demo_file]:
                zipf.write(item, arcname=os.path.basename(item))

        print(f"🪙 [ĐÚC THỎI VÀNG METAL THÀNH CÔNG]: Đã tạo '{zip_path}' ({os.path.getsize(zip_path)} bytes)!")
        return zip_path
