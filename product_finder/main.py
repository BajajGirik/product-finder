import asyncio
from crawler import Crawler
from web_browser import WebBrowserPool 
from time import time

async def crawl(domain):
    domain_crawler = Crawler(domain)

    await domain_crawler.crawl()
    
    print(f"{domain} urls saved")

async def main():
    start_time = time()
    print("Starting Script")

    await WebBrowserPool.setup()

    domains = ["amazon.in", "flipkart.com"]

    coros = [crawl(domain) for domain in domains]

    await asyncio.gather(*coros)

    total_time = round(time() - start_time, 2)
    print(
        f"Total time taken to find products for {len(domains)} domains: {total_time} seconds"
    )

if __name__ == "__main__":
    asyncio.run(main())
