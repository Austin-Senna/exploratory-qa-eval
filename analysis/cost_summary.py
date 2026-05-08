"""Quick cost summary across all agent_results.jsonl files."""
import json
from pathlib import Path
from collections import defaultdict


def as_float(value) -> float:
    try:
        return float(value or 0.0)
    except (TypeError, ValueError):
        return 0.0


def total_cost_with_ideal_subagents(record: dict) -> float:
    explicit = record.get("total_cost_with_ideal_subagents_usd")
    if explicit not in (None, ""):
        return as_float(explicit)
    return as_float(record.get("cost_usd")) + as_float(record.get("ideal_subagent_cost_usd"))

root = Path(__file__).parent.parent / "results"

totals = defaultdict(
    lambda: {
        "cost": 0.0,
        "ideal_subagent_cost": 0.0,
        "total_cost_with_ideal_subagents": 0.0,
        "tasks": 0,
        "input_tokens": 0,
        "output_tokens": 0,
        "failures": 0,
    }
)

for f in root.rglob("agent_results.jsonl"):
    # e.g. results/a/bedrock_claude-haiku-4.5-arn/agent_results.jsonl
    parts = f.relative_to(root).parts
    condition = parts[0] if len(parts) > 1 else "unknown"
    model = parts[1] if len(parts) > 2 else "unknown"
    key = f"{condition}/{model}"

    for line in f.read_text().splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        totals[key]["cost"] += as_float(r.get("cost_usd"))
        totals[key]["ideal_subagent_cost"] += as_float(r.get("ideal_subagent_cost_usd"))
        totals[key]["total_cost_with_ideal_subagents"] += total_cost_with_ideal_subagents(r)
        totals[key]["tasks"] += 1
        totals[key]["input_tokens"] += r.get("input_tokens", 0)
        totals[key]["output_tokens"] += r.get("output_tokens", 0)
        if not r.get("success", True) or r.get("error"):
            totals[key]["failures"] += 1

grand_total = 0.0
grand_ideal_subagent_total = 0.0
grand_combined_total = 0.0
print(
    f"\n{'Condition/Model':<45} {'Tasks':>6} {'Failures':>8} {'Input Tok':>12} "
    f"{'Output Tok':>12} {'Cost USD':>10} {'Ideal USD':>10} {'Total USD':>10}"
)
print("-" * 124)
for key, v in sorted(totals.items()):
    print(
        f"{key:<45} {v['tasks']:>6} {v['failures']:>8} "
        f"{v['input_tokens']:>12,} {v['output_tokens']:>12,} "
        f"${v['cost']:>9.4f} ${v['ideal_subagent_cost']:>9.4f} "
        f"${v['total_cost_with_ideal_subagents']:>9.4f}"
    )
    grand_total += v["cost"]
    grand_ideal_subagent_total += v["ideal_subagent_cost"]
    grand_combined_total += v["total_cost_with_ideal_subagents"]
print("-" * 124)
print(
    f"{'TOTAL':<45} {'':>6} {'':>8} {'':>12} {'':>12} "
    f"${grand_total:>9.4f} ${grand_ideal_subagent_total:>9.4f} "
    f"${grand_combined_total:>9.4f}"
)
