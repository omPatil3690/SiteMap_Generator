import json
from collections import deque
from urllib.parse import urlparse

from config import (
    MAX_DEPTH,
    MAX_PAGES
)


class SitemapCrawler:

    def __init__(
        self,
        client,
        graph
    ):
        self.client = client
        self.graph = graph

    def normalize_url(
        self,
        url
    ):

        return (
            url
            .split("#")[0]
            .rstrip("/")
        )

    def same_domain(
        self,
        root,
        target
    ):

        return (
            urlparse(root).netloc
            ==
            urlparse(target).netloc
        )

    async def extract_links(
        self,
        url
    ):

        prompt = f"""
Open:

{url}

Extract every internal hyperlink
visible on this page.

Return ONLY valid JSON.

Format:

{{
  "title": "Page Title",
  "links": [
      "https://example.com/about",
      "https://example.com/contact"
  ]
}}

No markdown.
No explanation.
Only JSON.
"""

        result = await self.client.run(
            prompt
        )

        try:

            data = json.loads(
                result.output
            )

            return data

        except Exception:

            return {
                "title": "",
                "links": []
            }

    async def crawl(
        self,
        start_url
    ):

        queue = deque()

        visited = set()

        queue.append(
            (
                start_url,
                0
            )
        )

        visited.add(
            start_url
        )

        pages_seen = 0

        while queue:

            if pages_seen >= MAX_PAGES:
                break

            current_url, depth = (
                queue.popleft()
            )

            if depth > MAX_DEPTH:
                continue

            print(
                f"Visiting: {current_url}"
            )

            page_data = (
                await self.extract_links(
                    current_url
                )
            )

            title = page_data.get(
                "title",
                ""
            )

            links = page_data.get(
                "links",
                []
            )

            self.graph.add_node(
                current_url,
                title
            )

            for link in links:

                link = self.normalize_url(
                    link
                )

                if not self.same_domain(
                    start_url,
                    link
                ):
                    continue

                self.graph.add_node(
                    link
                )

                self.graph.add_edge(
                    current_url,
                    link
                )

                if (
                    link
                    not in visited
                ):

                    visited.add(
                        link
                    )

                    queue.append(
                        (
                            link,
                            depth + 1
                        )
                    )

            pages_seen += 1