import re
from constants import SINGLE_PRODUCT_PATTERNS, PRODUCT_PATTERNS, NON_PRODUCT_PATTERNS
from .url import URLUtils

class RegexUtils:
    @staticmethod
    def get_product_url(url: str):
        url = URLUtils.get_url_without_query_params(url)

        # Handling amazon urls
        refIndex = url.find("/ref")

        if refIndex != -1:
            url = url[:refIndex]

        is_product_list_page = any(re.search(pattern, url) for pattern in PRODUCT_PATTERNS)
        is_single_product_page = any(re.search(pattern, url) for pattern in SINGLE_PRODUCT_PATTERNS)
        is_not_product_page = any(re.search(pattern, url) for pattern in NON_PRODUCT_PATTERNS)

        is_relevant_page = (is_product_list_page or is_single_product_page) and not is_not_product_page

        _url = url if is_relevant_page else ""

        return _url, is_single_product_page
