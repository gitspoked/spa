from __future__ import annotations

from typing import Protocol, Any


class GraphPersistenceAdapter(Protocol):
    """Boundary for FalkorDB or another persistent graph implementation."""

    def upsert_node(self, node_id: str, kind: str, properties: dict[str, Any]) -> None: ...
    def upsert_edge(self, source: str, relation: str, target: str, properties: dict[str, Any]) -> None: ...


class WorkflowRuntimeAdapter(Protocol):
    """Boundary for LangGraph or another durable workflow runtime."""

    def checkpoint(self, episode_id: str, state: dict[str, Any]) -> None: ...
    def resume(self, episode_id: str) -> dict[str, Any]: ...


class LearnedPredictorAdapter(Protocol):
    """ONNX/GNN boundary.

    A future implementation may run an ONNX model and return provisional direction,
    calibrated confidence, or expected information gain. It MUST NOT write a
    settlement state.
    """

    def predict(self, feature_graph: dict[str, Any]) -> dict[str, Any]: ...
