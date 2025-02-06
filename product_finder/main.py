import asyncio
from crawler import Crawler
from web_browser import WebBrowserPool 

async def crawl(domain):
    domain_crawler = Crawler(domain)

    await domain_crawler.crawl()
    
    print(f"{domain} urls saved")

async def main():
    await WebBrowserPool.setup()

    domains = ["amazon.in", "flipkart.com"]

    coros = [crawl(domain) for domain in domains]

    await asyncio.gather(*coros)

if __name__ == "__main__":
    asyncio.run(main())
