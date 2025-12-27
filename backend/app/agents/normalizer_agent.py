# app/agents/normalizer_agent.py
import re

class NormalizerAgent:

    REGION_MAP = {
        "경기": "경기도",
        "강원": "강원도",
        "충남": "충청남도",
        "충북": "충청북도",
        "전남": "전라남도",
        "전북": "전라북도",
        "경남": "경상남도",
        "경북": "경상북도",
    }

    def normalize(self, sql: str) -> str:
        """
        SQL 전체 정규화 entry point
        """
        sql = self.normalize_region(sql)
        return sql

    def normalize_region(self, sql: str) -> str:
    # 1️⃣ 축약어 → 정식명 + LIKE
        for short, full in self.REGION_MAP.items():
            sql = re.sub(
                rf"region\s*=\s*'{short}'",
                f"region LIKE '%{full}%'",
                sql,
                flags=re.IGNORECASE
            )

            sql = re.sub(
                rf"region\s*=\s*'{full}'",
                f"region LIKE '%{full}%'",
                sql,
                flags=re.IGNORECASE
            )

    # 2️⃣ 동일 컬럼 AND 조건 → OR 조건
        sql = re.sub(
            r"(region\s+LIKE\s+'%[^%]+%')\s+AND\s+(region\s+LIKE\s+'%[^%]+%')",
            r"(\1 OR \2)",
            sql,
            flags=re.IGNORECASE
        )

        return sql

