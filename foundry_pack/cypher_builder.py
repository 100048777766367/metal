class CypherScriptBuilder:
    @staticmethod
    def build_script(triplets):
        lines = [
            "// ============================================================",
            "// BODHI-METAL NEO4J GRAPH IMPORT SCRIPT (PRODUCTION GRADE)",
            "// ============================================================",
            "// Step 1: Ensure unique constraints on Entity Nodes",
            "CREATE CONSTRAINT IF NOT EXISTS FOR (e:Entity) REQUIRE e.id IS UNIQUE;\n",
            "// Step 2: Ingest verified knowledge triplets"
        ]
        for t in triplets:
            s = t["subject"].replace('"', '\\"')
            p = t["predicate"].upper().replace(" ", "_").replace("-", "_")
            o = t["object"].replace('"', '\\"')
            lines.append(f'MERGE (s:Entity {{id: "{s}"}}) MERGE (o:Entity {{id: "{o}"}}) MERGE (s)-[:{p} {{confidence: {t["confidence"]}}}]->(o);')
        return "\n".join(lines)
