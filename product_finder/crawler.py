from utils.file import FileSingleton
from web_browser import URLUtils, WebBrowserPool
from utils.regex import RegexUtils
import asyncio

class Crawler:
    max_depth = 1

    def __init__(self, domain) -> None:
        self.__domain = domain
        self.__product_urls = set()

    def get_product_urls(self):
        return self.__product_urls

    async def __crawl_page(self, url, depth):
        web_browser_id = None

        try: 
            web_browser_instance = await WebBrowserPool.get_instance()

            web_browser = web_browser_instance.web_browser
            web_browser_id = web_browser_instance.get_id()

            await web_browser.go_to_url(url)

            links = await web_browser.get_unique_links_on_page()

        except Exception as e:
            print(f"Error {url}: {e}")
            return
        finally:
            if web_browser_id is not None:
                WebBrowserPool.release(web_browser_id)

        new_links = []

        for link in links:
            _link =  link if link.startswith("http") else URLUtils.create_url_from_domain(self.__domain, link)
            product_url = RegexUtils.get_product_url(_link)

            if not product_url:
                continue

            if product_url in self.__product_urls:
                continue

            new_links.append(product_url)
            self.__product_urls.add(product_url)

        if depth >= Crawler.max_depth:
            return

        coros = [self.__crawl_page(link, depth + 1) for link in new_links]

        coros.append(FileSingleton.append_to_file(self.__domain, "\n".join(self.__product_urls)))

        await asyncio.gather(*coros)

    async def crawl(self):
        await self.__crawl_page(URLUtils.create_url_from_domain(self.__domain), 0)
