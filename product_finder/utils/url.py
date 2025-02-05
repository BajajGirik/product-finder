class URLUtils:
    @staticmethod
    def create_url_from_domain(domain):
        return f"https://{domain}"

    @staticmethod
    def get_url_without_query_params(url):
        return url.split("?")[0] if url is not None else ""

