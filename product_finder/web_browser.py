import asyncio
from typing import List
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
from utils.url import URLUtils
from playwright.async_api import async_playwright


class WebBrowser:
    def __init__(self) -> None:
        self.__last_scroll_height = 0
        self.__scroll_threshold = 10


    async def quit(self):
        await self.__instance.stop()


    async def setup(self):
        self.__instance = await async_playwright().start()
        browser = await self.__instance.chromium.launch(headless=False, args=[
            "--disable-gpu",
            "--disable-dev-shm-usage",  # Helps with memory in Docker
            "--no-sandbox",  # Required for running in some environments
            "--disable-background-networking",
            "--disable-background-timer-throttling",
            "--disable-backgrounding-occluded-windows",
            "--disable-renderer-backgrounding",
            "--disable-infobars",
            "--disable-extensions",
            "--blink-settings=imagesEnabled=false",  # Disables image loading
            "--mute-audio"
        ])
        self.__page = await browser.new_page()


    async def go_to_url(self, url, sleep_time = 2):
        # chrome_options = Options()
        # Run in background without spinning up GUI interface. (Improves efficiency)
        # chrome_options.add_argument("--headless")

        # Explicitly bypassing the security level in Docker with --no-sandbox
        # Docker deamon always runs as a root user, Chrome crashes.
        # chrome_options.add_argument("--no-sandbox")

        # Explicitly disabling the usage of /dev/shm/. The /dev/shm partition is
        # too small in certain VM environments, causing Chrome to fail or crash.
        # chrome_options.add_argument("--disable-dev-shm-usage")

        # Disabling image loading to improve efficiency
        # chrome_options.add_argument("--blink-settings=imagesEnabled=false")

        # self.__driver = webdriver.Chrome(options=chrome_options)

        # This is a bottleneck...Need to fix this
        # Would be better if web pages could be loaded asynchronously
        # self.__driver.get(url)

        await self.__page.goto(url)

        await asyncio.sleep(sleep_time)


    async def __get_scroll_height(self):
        return await self.__page.evaluate("document.body.scrollHeight")

    async def __scroll_to_bottom(self):
        self.__last_scroll_height = await self.__get_scroll_height()

        await self.__page.evaluate("window.scrollTo(0, document.body.scrollHeight);")

        await asyncio.sleep(2)

    async def get_unique_links_on_page(self):
        all_links = set()

        while True:
            elements = await self.__page.query_selector_all("a")

            for element in elements:
                url = await element.get_attribute("href")
                if url is None:
                    continue

                # Improve dedup logic
                url = URLUtils.get_url_without_query_params(url)

                if url not in all_links:
                    all_links.add(url)

            await self.__scroll_to_bottom()

            if (await self.__get_scroll_height()) - self.__last_scroll_height < self.__scroll_threshold:
                break

        return all_links


class WebBrowserPoolItem:
    def __init__(self, id: int, web_browser: WebBrowser) -> None:
        self.__id = id
        self.web_browser = web_browser
        self.__is_available = True
        
    def get_id(self):
        return self.__id

    def is_available(self):
        return self.__is_available

    def set_available(self, is_available):
        self.__is_available = is_available


CONCURRENT_BROWSERS = 20

class WebBrowserPool:
    __concurrent_browsers = CONCURRENT_BROWSERS
    __pool: List[WebBrowserPoolItem] = []
    __semaphore = asyncio.Semaphore(CONCURRENT_BROWSERS)
    __lock = asyncio.Lock()

    @staticmethod
    async def setup_single_browser():
        web_browser = WebBrowser()
        await web_browser.setup()
        return web_browser


    @staticmethod
    async def get_instance():
        async with WebBrowserPool.__lock:
            if len(WebBrowserPool.__pool) == 0:
                coros = [WebBrowserPool.setup_single_browser() for _ in range(WebBrowserPool.__concurrent_browsers)]

                web_browsers = await asyncio.gather(*coros)

                for web_browser in web_browsers:
                    pool_item = WebBrowserPoolItem(len(WebBrowserPool.__pool), web_browser)
                    WebBrowserPool.__pool.append(pool_item)

        await WebBrowserPool.__semaphore.acquire()

        for item in WebBrowserPool.__pool:
            if item.is_available():
                item.set_available(False)
                return item

        raise Exception("No available browsers")

    @staticmethod
    def release(id):
        WebBrowserPool.__pool[id].set_available(True)
        WebBrowserPool.__semaphore.release()
