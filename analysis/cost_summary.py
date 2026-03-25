"""Quick cost summary across all agent_results.jsonl files."""
import json
from pathlib import Path
from collections import defaultdict

root = Path(__file__).parent.parent / "results"

totals = defaultdict(lambda: {"cost": 0.0, "tasks": 0, "input_tokens": 0, "output_tokens": 0, "failures": 0})

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
        totals[key]["cost"] += r.get("cost_usd", 0)
        totals[key]["tasks"] += 1
        totals[key]["input_tokens"] += r.get("input_tokens", 0)
        totals[key]["output_tokens"] += r.get("output_tokens", 0)
        if not r.get("success", True) or r.get("error"):
            totals[key]["failures"] += 1

grand_total = 0.0
print(f"\n{'Condition/Model':<45} {'Tasks':>6} {'Failures':>8} {'Input Tok':>12} {'Output Tok':>12} {'Cost USD':>10}")
print("-" * 100)
for key, v in sorted(totals.items()):
    print(f"{key:<45} {v['tasks']:>6} {v['failures']:>8} {v['input_tokens']:>12,} {v['output_tokens']:>12,} ${v['cost']:>9.4f}")
    grand_total += v["cost"]
print("-" * 100)
print(f"{'TOTAL':<45} {'':>6} {'':>8} {'':>12} {'':>12} ${grand_total:>9.4f}")
