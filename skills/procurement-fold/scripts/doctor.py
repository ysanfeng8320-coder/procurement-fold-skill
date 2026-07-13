#!/usr/bin/env python3
"""procurement-fold 环境自检 — 发给别人用之前先跑这个。"""
from __future__ import annotations

import os
import sys

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.normpath(os.path.join(SKILL_DIR, "..", ".."))


def ok(msg: str) -> None:
    print(f"  ✓ {msg}")


def bad(msg: str) -> None:
    print(f"  ✗ {msg}")


def main() -> int:
    print(f"REPO = {REPO}")
    print(f"SKILL = {SKILL_DIR}")
    errors = 0

    def need(path: str, label: str) -> None:
        nonlocal errors
        p = os.path.join(REPO, path) if not os.path.isabs(path) else path
        if os.path.exists(p):
            ok(label)
        else:
            bad(f"缺少 {label}: {p}")
            errors += 1

    need("kg_engine", "kg_engine/")
    need("kg_engine/fold/run_v2.py", "fold.run_v2")
    need("kg_engine/fold/scene_fit.py", "fold.scene_fit")
    need("kg_engine/fold/phone_complete.py", "fold.phone_complete")
    need("kg_engine/fold/acquisition_gate.py", "fold.acquisition_gate")
    need("kg_engine/phone_enricher.py", "phone_enricher")
    need("skills/procurement-fold/SKILL.md", "SKILL.md")
    need("skills/procurement-fold/ORCHESTRATION.md", "ORCHESTRATION.md")
    need("skills/procurement-fold/config/acquisition_gate.yaml", "acquisition_gate.yaml")
    need("skills/procurement-fold/product_packs/seal_control/lexicon.yaml", "product seal_control")
    need("skills/procurement-fold/species_packs/court/species.yaml", "species court")

    scout = os.path.join(REPO, "scout_data")
    if os.path.isdir(scout):
        n = len([x for x in os.listdir(scout) if x.endswith(".json")])
        ok(f"scout_data/ ({n} json)")
    else:
        bad("scout_data/ 不存在（可空目录，但建议有本地缓存）")
        errors += 1

    try:
        import yaml  # noqa: F401
        ok("PyYAML")
    except ImportError:
        bad("未安装 PyYAML（pip install pyyaml）")
        errors += 1

    # import engine
    sys.path.insert(0, os.path.join(REPO, "kg_engine"))
    try:
        from fold.pack_loader import load_pack
        from fold.species_loader import load_species
        load_pack("seal_control")
        load_species("court")
        ok("load_pack(seal_control) + load_species(court)")
    except Exception as e:
        bad(f"引擎加载失败: {e}")
        errors += 1

    fold_runs = os.path.join(REPO, "fold_runs")
    os.makedirs(fold_runs, exist_ok=True)
    ok("fold_runs/ 可写")

    print()
    if errors:
        print(f"FAILED ({errors} issues). 请在仓库根目录修复后再跑 skill。")
        return 1
    print("OK — procurement-fold 可被 Codex / Workflow 使用。")
    print("下一步示例:")
    print("  python3 skills/procurement-fold/scripts/run_fold.py --species court --portfolio seal_control --reuse-local --api-budget 0 --phone-complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
