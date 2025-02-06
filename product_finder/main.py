import asyncio
from crawler import Crawler 

async def crawl(domain):
    domain_crawler = Crawler(domain)

    await domain_crawler.crawl()
    
    print(f"{domain} urls saved")

async def main():
    domains = ["amazon.in", "flipkart.com"]

    # tasks = [asyncio.create_task(crawl_and_save_results(domain)) for domain in domains]
    coros = [crawl(domain) for domain in domains]

    await asyncio.gather(*coros)

if __name__ == "__main__":
    asyncio.run(main())
