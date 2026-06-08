import json
from collections import deque
from urllib.parse import urlparse

from browser_use import Agent, ChatOpenAI
from browser_use import Agent

from config import (
    MAX_DEPTH,
    MAX_PAGES
)


class SitemapCrawler:

    def __init__(
        self,
        graph
    ):
        self.graph = graph

        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.0,
        )

    def normalize_url(
        self,
        url
    ):

        if not url:
            return ""

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

        try:

            root_domain = ".".join(
                urlparse(root)
                .netloc
                .split(".")[-2:]
            )

            target_domain = ".".join(
                urlparse(target)
                .netloc
                .split(".")[-2:]
            )

            return (
                root_domain
                ==
                target_domain
            )

        except Exception:

            return False

    async def extract_links(
        self,
        url
    ):

        task = f"""
Visit:

{url}

Extract all visible hyperlinks on this page.

Return ONLY a valid JSON object.

Format:

{{
    "title": "Page Title",
    "links": [
        "https://example.com/page1",
        "https://example.com/page2"
    ]
}}

No markdown.
No explanation.
No code blocks.
Only JSON.
"""

        try:

            agent = Agent(
                task=task,
                llm=self.llm,
            )

            result = await agent.run()

            print("\n" + "=" * 60)
            print(f"PAGE: {url}")
            print("=" * 60)

            try:

                output = result.final_result()

            except Exception:

                output = result

            print("RAW OUTPUT:")
            print(output)

            # Already parsed dictionary
            if isinstance(
                output,
                dict
            ):
                return output

            # String JSON
            if isinstance(
                output,
                str
            ):

                try:

                    parsed = json.loads(
                        output
                    )

                    return parsed

                except Exception:

                    print(
                        "JSON parsing failed"
                    )

                    return {
                        "title": "",
                        "links": []
                    }

            print(
                "Unexpected output type:"
            )

            print(type(output))

            return {
                "title": "",
                "links": []
            }

        except Exception as e:

            print(
                f"Failed extracting links from {url}"
            )

            print(e)

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

        start_url = self.normalize_url(
            start_url
        )

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

                print(
                    f"Reached MAX_PAGES={MAX_PAGES}"
                )

                break

            current_url, depth = (
                queue.popleft()
            )

            if depth > MAX_DEPTH:
                continue

            print(
                f"\nVisiting: {current_url}"
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

            print(
                f"Found {len(links)} links"
            )

            self.graph.add_node(
                current_url,
                title
            )

            for link in links:

                link = (
                    self.normalize_url(
                        link
                    )
                )

                if not link:
                    continue

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

        print("\n" + "=" * 60)
        print("CRAWL COMPLETE")
        print("=" * 60)

        print(
            f"Pages Crawled: {pages_seen}"
        )

        print(
            f"Nodes Found: {len(self.graph.nodes)}"
        )

        edge_count = sum(
            len(targets)
            for targets
            in self.graph.edges.values()
        )

        print(
            f"Edges Found: {edge_count}"
        )