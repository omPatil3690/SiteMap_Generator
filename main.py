import asyncio

from browser_use_sdk.v3 import (
    AsyncBrowserUse
)

from crawler import SitemapCrawler
from graph import SiteGraph
from exporter import (
    export_json,
    export_mermaid
)


async def main():

    START_URL = (
        "https://example.com"
    )

    client = AsyncBrowserUse()

    graph = SiteGraph()

    crawler = SitemapCrawler(
        client,
        graph
    )

    await crawler.crawl(
        START_URL
    )

    export_json(
        graph,
        "output/sitemap.json"
    )

    export_mermaid(
        graph,
        "output/sitemap.mmd"
    )

    print(
        "Sitemap generation complete."
    )


if __name__ == "__main__":
    asyncio.run(main())