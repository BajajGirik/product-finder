import asyncio
from crawler import Crawler 
from utils.file import FileSingleton

async def crawl_and_save_results(domain):
    domain_crawler = Crawler(domain)

    urls = await domain_crawler.crawl()

    urls = "\n".join(urls)

    await FileSingleton.append_to_file(urls)
    
    print(f"{domain} urls saved")

async def main():
    domains = ["amazon.in", "flipkart.com"]

    # tasks = [asyncio.create_task(crawl_and_save_results(domain)) for domain in domains]
    coros = [crawl_and_save_results(domain) for domain in domains]

    await asyncio.gather(*coros)

if __name__ == "__main__":
    asyncio.run(main())
