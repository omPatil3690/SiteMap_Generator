import asyncio
from browser_use_sdk.v3 import AsyncBrowserUse


async def main():

    client = AsyncBrowserUse()

    result = await client.run(
        """
Open:

https://www.langchain.com/

Extract every internal hyperlink
visible on this page.

take only top 10 links

"""
    )

    print(result.output)


asyncio.run(main())