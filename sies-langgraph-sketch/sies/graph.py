from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Node:
    node_id: str
    kind: str
    properties: dict[str, Any]


@dataclass(frozen=True)
class Edge:
    source: str
    relation: str
    target: str
    properties: dict[str, Any]


class PropertyGraph:
    """Minimal graph IR intended to map later to FalkorDB or another property graph."""

    def __init__(self) -> None:
        self.nodes: dict[str, Node] = {}
        self.edges: list[Edge] = []

    def add_node(self, node_id: str, kind: str, **properties: Any) -> Node:
        node = Node(node_id, kind, dict(properties))
        self.nodes[node_id] = node
        return node

    def add_edge(self, source: str, relation: str, target: str, **properties: Any) -> Edge:
        if source not in self.nodes or target not in self.nodes:
            raise KeyError("Both edge endpoints must already exist")
        edge = Edge(source, relation, target, dict(properties))
        self.edges.append(edge)
        return edge

    def neighbors(self, node_id: str, incoming: bool = False) -> list[Edge]:
        if incoming:
            return [e for e in self.edges if e.target == node_id]
        return [e for e in self.edges if e.source == node_id]
