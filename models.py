from dataclasses import dataclass


@dataclass
class PageNode:
    url: str
    title: str = ""