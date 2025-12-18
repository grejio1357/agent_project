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
        sql = self.normalize_region(sql)
        return sql

    def normalize_region(self, sql: str) -> str:
        for short, full in self.REGION_MAP.items():
            sql = re.sub(
                rf"(region\s*=\s*'{short}')",
                f"region = '{full}'",
                sql
            )
        return sql
