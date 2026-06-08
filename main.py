import asyncio

from crawler import SitemapCrawler
from graph import SiteGraph
from exporter import (
    export_json,
    export_mermaid
)


async def main():

    START_URL = (
        "https://www.invimatic.com/"
    )

    graph = SiteGraph()

    crawler = SitemapCrawler(
        graph
    )

    await crawler.crawl(
        START_URL
    )

    print("\nNodes:")
    print(graph.nodes)

    print("\nEdges:")
    print(dict(graph.edges))

    print("\nCrawl Complete")

    export_json(
        graph,
        "output/sitemap.json"
    )

    export_mermaid(
        graph,
        "output/sitemap.mmd"
    )

    print(
        "\nSitemap generation complete."
    )


if __name__ == "__main__":
    asyncio.run(main())