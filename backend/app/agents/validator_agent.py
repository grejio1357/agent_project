import re


class ValidatorAgent:
    """
    Validate and fix generated SQL before execution.
    Day 3 scope:
    - Region name normalization
    - Replace '=' with LIKE for region matching
    """

    REGION_MAP = {
        "경기": "경기도",
        "서울": "서울특별시",
        "부산": "부산광역시",
        "충북": "충청북도",
        "충남": "충청남도",
        "전북": "전라북도",
        "전남": "전라남도",
        "경북": "경상북도",
        "경남": "경상남도",
        "제주": "제주특별자치도",
    }

    def run(self, sql: str) -> str:
        sql = self._normalize_region(sql)
        sql = self._use_like_for_region(sql)
        return sql

    def _normalize_region(self, sql: str) -> str:
        """
        Replace abbreviated region names with full names.
        """
        for short, full in self.REGION_MAP.items():
            # region = '경기'
            sql = re.sub(
                rf"region\s*=\s*'{short}'",
                f"region = '{full}'",
                sql
            )
        return sql

    def _use_like_for_region(self, sql: str) -> str:
        """
        Change region equality to LIKE for flexible matching.
        """
        sql = re.sub(
            r"region\s*=\s*'([^']+)'",
            r"region LIKE '%\1%'",
            sql
        )
        return sql