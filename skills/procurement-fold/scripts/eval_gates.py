#!/usr/bin/env python3
"""Eval gates for procurement-fold v2 goal: actionable species×product customers."""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

# Gap lead types that count toward actionable customer lists
GAP_TYPES = frozenset({"assoc_gap", "peer_gap"})

GATES = [
    ("G1_events_ge_20", "species×product events >= 20"),
    ("G2_action_events_ge_3", "action-region product events >= 3"),
    ("G3_has_assoc_gap", "at least one assoc_gap or peer_gap lead"),
    ("G4_gap_evidence_ok", "gap leads have matched_keyword evidence"),
    ("G5_leads_ge_5", "leads >= 5"),
    ("G6_not_prior_only", "score not prior-only (gap+strong+peer units >= 3)"),
]


def eval_run(run_dir: Path) -> dict:
    meta = json.loads((run_dir / "run_meta.json").read_text(encoding="utf-8"))
    scores = json.loads((run_dir / "portfolio_scores.json").read_text(encoding="utf-8"))
    leads = json.loads((run_dir / "leads.json").read_text(encoding="utf-8"))
    events_path = run_dir / "events.jsonl"
    events = []
    if events_path.exists():
        events = [json.loads(l) for l in events_path.read_text(encoding="utf-8").splitlines() if l.strip()]

    action = meta.get("action_regions") or []
    action_events = [e for e in events if e.get("region") in action]
    gap_leads = [l for l in leads if l.get("lead_type") in GAP_TYPES]
    bad_ev = 0
    for lead in gap_leads:
        evs = lead.get("evidence") or []
        if not evs:
            bad_ev += 1
            continue
        if not any(e.get("matched_keyword") for e in evs):
            bad_ev += 1
    fac = (scores[0].get("factors") if scores else {}) or {}
    peer_n = sum(1 for l in leads if l.get("lead_type") == "peer_gap")
    signal_units = (
        fac.get("gap_units", 0)
        + fac.get("strong_units", 0)
        + peer_n
    )

    results = {
        "G1_events_ge_20": len(events) >= 20,
        "G2_action_events_ge_3": len(action_events) >= 3,
        "G3_has_assoc_gap": len(gap_leads) >= 1,
        "G4_gap_evidence_ok": len(gap_leads) >= 1 and bad_ev == 0,
        "G5_leads_ge_5": len(leads) >= 5,
        "G6_not_prior_only": signal_units >= 3,
    }
    passed = sum(1 for v in results.values() if v)
    verdict = "USABLE" if passed >= 5 else "NOT_USABLE"
    return {
        "run_dir": str(run_dir),
        "passed": passed,
        "total": len(results),
        "verdict": verdict,
        "gates": results,
        "stats": {
            "events": len(events),
            "action_events": len(action_events),
            "leads": len(leads),
            "lead_types": dict(Counter(l.get("lead_type") for l in leads)),
            "event_regions": dict(Counter(e.get("region") for e in events)),
            "score": scores[0] if scores else None,
        },
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("run_dir", nargs="?", help="fold_runs/<id>")
    p.add_argument("--latest-police", action="store_true")
    p.add_argument("--latest-court", action="store_true")
    p.add_argument("--latest", metavar="SPECIES", help="latest fold_runs/*_<species>")
    args = p.parse_args()
    root = Path(__file__).resolve().parents[3] / "fold_runs"
    if args.latest:
        suffix = f"_{args.latest}"
        runs = sorted(root.glob(f"*{suffix}"), key=lambda x: x.stat().st_mtime)
        if not runs:
            print(f"No runs matching *{suffix}", file=sys.stderr)
            sys.exit(2)
        run_dir = runs[-1]
    elif args.latest_court:
        runs = sorted(root.glob("*_court"), key=lambda x: x.stat().st_mtime)
        if not runs:
            print("No court runs found", file=sys.stderr)
            sys.exit(2)
        run_dir = runs[-1]
    elif args.latest_police or not args.run_dir:
        runs = sorted(root.glob("*_police"), key=lambda x: x.stat().st_mtime)
        if not runs:
            print("No police runs found", file=sys.stderr)
            sys.exit(2)
        run_dir = runs[-1]
    else:
        run_dir = Path(args.run_dir)

    out = eval_run(run_dir)
    print(json.dumps(out, ensure_ascii=False, indent=2))
    sys.exit(0 if out["verdict"] == "USABLE" else 1)


if __name__ == "__main__":
    main()
