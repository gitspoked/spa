#!/usr/bin/env python3
"""
On-the-fly diagram utility for DLC process flows.

Produces:
- Mermaid source (.mmd) ready for any Mermaid renderer
- Optional simple matplotlib flowchart PNGs for quick static images
- Receipt-linked scenario captions

Usage:
  python3 diagram_util.py lifecycle
  python3 diagram_util.py conflict
  python3 diagram_util.py gates
  python3 diagram_util.py all
"""

from __future__ import annotations

import sys
from pathlib import Path

OUT = Path(__file__).parent / "generated-diagrams"
OUT.mkdir(exist_ok=True)

MERMAID = {
    "lifecycle": """flowchart TD
    A[Claim C] --> B{Confidence contract satisfied?}
    B -->|Yes| C[Emit provisional ResponseReceipt]
    B -->|No| D[Skip provisional]
    C --> E[Parallel Evidence Collection]
    D --> E
    E --> F[Deterministic Settler]
    F --> G{State}
    G -->|PASS| H[SettlementReceipt PASS]
    G -->|FAIL| I[SettlementReceipt FAIL]
    G -->|CONFLICT| J[SettlementReceipt CONFLICT]
    G -->|INDETERMINATE| K[SettlementReceipt INDETERMINATE]
    H --> L{Mismatch?}
    I --> L
    J --> L
    K --> L
    L -->|Yes| M[LearningEvent]
    L -->|No| N[Continue]
    M --> O[Optional Amendment]
    O --> P[Gate decision]
    N --> P
""",
    "conflict": """flowchart LR
    E[Evidence<br/>3 PASS + 2 FAIL + 25 MISSING] --> S[Settler]
    S --> C[SettlementReceipt CONFLICT]
    C --> Q[Quarantine as premise]
    C --> L[LearningEvent]
    L --> A[AmendmentProposal]
""",
    "gates": """stateDiagram-v2
    [*] --> Gate0
    Gate0 --> Gate1: structure consistent
    Gate1 --> Gate2
    Gate2 --> Gate3
    Gate3 --> Gate4: receipts
    Gate4 --> GateN
    Gate3 --> Gate3: INDETERMINATE hold
    Gate4 --> Gate4: amendment quarantined
""",
    "self-adjust": """flowchart TD
    LE[LearningEvent] --> AP[AmendmentProposal]
    AP --> EV[Collect evidence]
    EV --> ST{Settlement}
    ST -->|PASS| UP[New artifact digest]
    ST -->|other| QZ[Quarantine]
    UP --> CAN[Canonical updated]
    QZ --> HOLD[Process unchanged]
""",
}


def write_mermaid(name: str) -> Path:
    p = OUT / f"{name}.mmd"
    p.write_text(MERMAID[name])
    print(f"Wrote {p}")
    return p


def try_matplotlib(name: str) -> None:
    try:
        import matplotlib.pyplot as plt
        import matplotlib.patches as mpatches
    except ImportError:
        print("matplotlib not available — skipping PNG")
        return

    fig, ax = plt.subplots(figsize=(12, 7))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.axis("off")
    ax.set_facecolor("#0d1117")
    fig.patch.set_facecolor("#0d1117")

    def box(x, y, w, h, text, color="#1f6feb"):
        ax.add_patch(mpatches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05",
                                             facecolor=color, edgecolor="#58a6ff", linewidth=1.5))
        ax.text(x + w/2, y + h/2, text, ha="center", va="center", color="white", fontsize=9, wrap=True)

    if name == "lifecycle":
        box(4, 7, 2, 0.6, "Claim C")
        box(3.5, 5.8, 3, 0.6, "Parallel Evidence")
        box(3.5, 4.6, 3, 0.6, "Deterministic Settler")
        box(1, 3, 1.8, 0.7, "PASS")
        box(3, 3, 1.8, 0.7, "FAIL")
        box(5, 3, 1.8, 0.7, "CONFLICT", "#da3633")
        box(7, 3, 1.8, 0.7, "INDET")
        box(3.5, 1.5, 3, 0.6, "LearningEvent / Gate")
        ax.set_title("Lifecycle (simplified)", color="white")
    elif name == "conflict":
        box(1, 4, 2.5, 1.2, "3 PASS\n2 FAIL\n25 MISSING")
        box(4.5, 4.3, 1.5, 0.8, "Settler")
        box(7, 4, 2.2, 1, "CONFLICT", "#da3633")
        box(2, 1.5, 2, 0.8, "Quarantine")
        box(6, 1.5, 2.5, 0.8, "LearningEvent → Amend")
        ax.set_title("CONFLICT Scenario", color="white")
    else:
        box(1, 4, 1.5, 0.7, "Gate0")
        box(3, 4, 1.5, 0.7, "Gate1")
        box(5, 4, 1.5, 0.7, "Gate2")
        box(7, 4, 1.5, 0.7, "Gate3")
        ax.set_title("Gate Progression (partial)", color="white")

    png = OUT / f"{name}.png"
    fig.savefig(png, dpi=120, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close()
    print(f"Wrote {png}")


def main():
    targets = sys.argv[1:] or ["all"]
    if "all" in targets:
        targets = list(MERMAID.keys())
    for t in targets:
        if t not in MERMAID:
            print(f"Unknown: {t}. Choose from {list(MERMAID)}")
            continue
        write_mermaid(t)
        try_matplotlib(t)
    print(f"\nOutput directory: {OUT}")
    print("Render .mmd files with any Mermaid live editor or mmdc.")


if __name__ == "__main__":
    main()
