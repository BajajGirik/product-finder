from web_browser import URLUtils, WebBrowser
from utils.regex import RegexUtils
import asyncio

class Crawler:
    max_depth = 1

    def __init__(self, domain) -> None:
        self.__domain = domain
        self.__product_urls = set()
        self.__visited_urls = set()

    def get_product_urls(self):
        return self.__product_urls

    async def __crawl_page(self, url, depth):
        if url in self.__visited_urls:
            return

        web_browser = WebBrowser()

        self.__visited_urls.add(url)

        await web_browser.go_to_url(url)

        print(f"Visiting {url}")
        links = await web_browser.get_unique_links_on_page()

        print(f"Get Links {url}")

        await web_browser.quit()
        print(f"Quitting {url}")

        new_links = []

        for link in links:
            if RegexUtils.is_product_url(link):
                new_links.append(link)
                self.__product_urls.add(link)

        if depth > Crawler.max_depth:
            return

        coros = [self.__crawl_page(link, depth + 1) for link in new_links]

        await asyncio.gather(*coros)

    async def crawl(self):
        await self.__crawl_page(URLUtils.create_url_from_domain(self.__domain), 0)
        return self.__product_urls
