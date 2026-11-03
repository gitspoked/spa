# SIES + Content-Addressed Parallel Node Sketch

Minimal runner for the receipted speculative graph:

- Node identity = SHA-256 of memory + tools contents
- Parallel speculative execution → response receipts + evidence observations
- Deterministic settler → settlement receipts
- Four states: INDETERMINATE / PASS / FAIL / CONFLICT
- Answer sufficiency (confidence contract) is separate from settlement completeness

## Run
```bash
cd sies-langgraph-sketch
python3 sketch.py
```

Nodes can later be replaced by LangGraph nodes or containerized MKZ executors without changing the receipt/settlement contract.
