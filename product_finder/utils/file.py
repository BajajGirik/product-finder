import asyncio
import aiofiles

class FileSingleton:
    filename = "products_2.txt"

    @staticmethod
    async def append_to_file(content):
        try:
            async with asyncio.Lock():
                async with aiofiles.open(FileSingleton.filename, "a") as f:
                    await f.write(content + "\n")
        except Exception as e:
            print(f"Error writing to file {FileSingleton.filename}: {e}")
