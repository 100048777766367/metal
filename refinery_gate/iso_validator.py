import re

class IsoCleanroomValidator:
    EMAIL_PATT = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    PHONE_PATT = r'\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b'
    IP_PATT    = r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'

    @classmethod
    def sanitize_triplet(cls, item):
        s = str(item.get("subject", "")).strip()
        p = str(item.get("predicate", "")).strip().lower().replace(" ", "_")
        o = str(item.get("object", "")).strip()

        # Cắt bỏ nếu dính văn bản báo chí dài (>75 ký tự) hoặc quá ngắn
        if len(s) > 75 or len(o) > 75 or len(s) < 2 or len(p) < 2 or len(o) < 2:
            return None

        # Khử trùng Zero-PII
        for text in [s, o]:
            if re.search(cls.EMAIL_PATT, text) or re.search(cls.PHONE_PATT, text) or re.search(cls.IP_PATT, text):
                return None

        clean_s = re.sub(r'[^\w\s\-_]', '', s).strip().capitalize()
        clean_p = re.sub(r'[^\w\s\-_]', '', p).strip()
        clean_o = re.sub(r'[^\w\s\-_]', '', o).strip().capitalize()

        return {"subject": clean_s, "predicate": clean_p, "object": clean_o, "confidence": float(item.get("confidence", 0.98))}
