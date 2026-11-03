from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import re


_WIKILINK = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")


@dataclass(frozen=True)
class KnowledgeObject:
    logical_path: str
    digest: str
    content: bytes
    previous_digest: str | None
    wikilinks: tuple[str, ...]


class MarkdownKnowledgeStore:
    """In-memory content-addressed reference store for scrubbed Markdown."""

    def __init__(self) -> None:
        self.objects: dict[str, KnowledgeObject] = {}
        self.heads: dict[str, str] = {}

    def ingest(self, logical_path: str, markdown: str) -> KnowledgeObject:
        content = markdown.encode("utf-8")
        digest = f"sha256:{sha256(content).hexdigest()}"
        previous = self.heads.get(logical_path)
        links = tuple(dict.fromkeys(m.strip() for m in _WIKILINK.findall(markdown)))
        obj = KnowledgeObject(logical_path, digest, content, previous, links)
        self.objects.setdefault(digest, obj)
        self.heads[logical_path] = digest
        return obj

    def get(self, digest: str) -> KnowledgeObject:
        return self.objects[digest]
