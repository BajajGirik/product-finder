import re
from constants import PRODUCT_PATTERNS

class RegexUtils:
    @staticmethod
    def is_product_url(url):
        return any(re.search(pattern, url) for pattern in PRODUCT_PATTERNS)

