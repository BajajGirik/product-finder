class URLUtils:
    @staticmethod
    def create_url_from_domain(domain, path = ""):
        _path = path if path.startswith("/") else f"/{path}"
        return f"https://{domain}{_path}"

    @staticmethod
    def get_url_without_query_params(url):
        return url.split("?")[0] if url is not None else ""

