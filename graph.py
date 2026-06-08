from collections import defaultdict


class SiteGraph:

    def __init__(self):
        self.nodes = {}
        self.edges = defaultdict(set)

    def add_node(
        self,
        url,
        title=""
    ):
        self.nodes[url] = {
            "url": url,
            "title": title
        }

    def add_edge(
        self,
        source,
        target
    ):
        self.edges[source].add(target)

    def to_dict(self):

        return {
            "nodes": list(
                self.nodes.values()
            ),
            "edges": [
                {
                    "source": source,
                    "target": target
                }
                for source, targets
                in self.edges.items()
                for target in targets
            ]
        }