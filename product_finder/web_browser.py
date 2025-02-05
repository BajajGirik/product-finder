import asyncio
from typing import Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from utils.url import URLUtils
from playwright.async_api import async_playwright


class WebBrowser:
    semaphore = asyncio.Semaphore(15)

    def __init__(self) -> None:
        self.__last_scroll_height = 0
        self.__scroll_threshold = 10


    async def quit(self):
        await self.__instance.stop()
        WebBrowser.semaphore.release()


    async def go_to_url(self, url, sleep_time = 1):
        await WebBrowser.semaphore.acquire()

        self.__instance = await async_playwright().start()
        browser = await self.__instance.chromium.launch()

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

        self.__page = await browser.new_page()
        await self.__page.goto(url)


    async def __get_scroll_height(self):
        return await self.__page.evaluate("document.body.scrollHeight")

    async def __scroll_to_bottom(self):
        self.__last_scroll_height = await self.__get_scroll_height()

        await self.__page.evaluate("window.scrollTo(0, document.body.scrollHeight);")

        await asyncio.sleep(2)

    async def get_unique_links_on_page(self):
        # Todo: Handle infinite scroll
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
