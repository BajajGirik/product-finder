import re
from constants import PRODUCT_PATTERNS, NON_PRODUCT_PATTERNS
from .url import URLUtils

class RegexUtils:
    @staticmethod
    def get_product_url(url: str):
        url = URLUtils.get_url_without_query_params(url)

        # Handling amazon urls
        refIndex = url.find("/ref")

        if refIndex != -1:
            url = url[:refIndex]

        return url if any(re.search(pattern, url) for pattern in PRODUCT_PATTERNS) and not any(re.search(pattern, url) for pattern in NON_PRODUCT_PATTERNS) else ""
