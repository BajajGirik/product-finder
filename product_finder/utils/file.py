import asyncio
import aiofiles

class FileSingleton:
    __suffix = "products.txt"
    __locks = {}

    @staticmethod
    async def append_to_file(domain, content):
        if domain not in FileSingleton.__locks:
            FileSingleton.__locks[domain] = asyncio.Lock()

        filename = f"{domain}_{FileSingleton.__suffix}"

        try:
            async with FileSingleton.__locks[domain]:
                async with aiofiles.open(f"outputs/{filename}", "a") as f:
                    await f.write(content + "\n")
        except Exception as e:
            print(f"Error writing to file {filename}: {e}")
