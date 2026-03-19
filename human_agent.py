#!/usr/bin/env python3
"""
Interactive human-agent REPL.

Lets you manually run a benchmark task using the same tools the LLM agent has:
  search, search_keyword, list_files, inspect_file, download, execute_code, submit_answer

Usage:
    python human_agent.py                          # pick a random task
    python human_agent.py --task tasks/k-3-d-3/task_3.json
    python human_agent.py --question "What is ..."
    python human_agent.py --use-aurum              # also enable aurum tools
"""

import argparse
import json
import os
import random
import sys
import textwrap
import time
from pathlib import Path

# ---------------------------------------------------------------------------
# Bootstrap path so we can import from evaluation/
# ---------------------------------------------------------------------------
_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(_ROOT))

from evaluation.tools import agent_tools

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _pp(obj, indent=2):
    """Pretty-print a dict/list."""
    print(json.dumps(obj, indent=indent, default=str))


def _banner(text, width=70, char="="):
    print(char * width)
    for line in textwrap.wrap(text, width - 4):
        print(f"  {line}")
    print(char * width)


def _short(obj, max_chars=2000):
    """Truncate long output for display."""
    s = json.dumps(obj, indent=2, default=str)
    if len(s) > max_chars:
        return s[:max_chars] + f"\n... [{len(s) - max_chars} chars truncated]"
    return s


# ---------------------------------------------------------------------------
# Tool wrappers with friendly I/O
# ---------------------------------------------------------------------------

def cmd_search(use_aurum: bool):
    raw = input("  prefixes (comma-separated): ").strip()
    prefixes = [p.strip() for p in raw.split(",") if p.strip()]
    if not prefixes:
        print("  [!] No prefixes given.")
        return
    t0 = time.time()
    result = agent_tools.search(prefixes)
    print(f"  [{time.time()-t0:.1f}s]")
    print(_short(result))


def cmd_search_keyword(use_aurum: bool):
    raw = input("  keywords (comma-separated): ").strip()
    keywords = [k.strip() for k in raw.split(",") if k.strip()]
    if not keywords:
        print("  [!] No keywords given.")
        return
    limit_raw = input("  limit [20]: ").strip()
    limit = int(limit_raw) if limit_raw.isdigit() else 20
    t0 = time.time()
    result = agent_tools.search_keyword(keywords, limit=limit)
    print(f"  [{time.time()-t0:.1f}s]")
    print(_short(result))


def cmd_list_files(use_aurum: bool):
    raw = input("  dataset_ids (comma-separated): ").strip()
    ids = [d.strip() for d in raw.split(",") if d.strip()]
    if not ids:
        print("  [!] No dataset ids given.")
        return
    t0 = time.time()
    result = agent_tools.list_files(ids)
    print(f"  [{time.time()-t0:.1f}s]")
    print(_short(result))


def cmd_inspect_file(use_aurum: bool):
    dataset_id = input("  dataset_id: ").strip()
    file_path = input("  file_path: ").strip()
    if not dataset_id or not file_path:
        print("  [!] Both dataset_id and file_path required.")
        return
    t0 = time.time()
    result = agent_tools.inspect_file(dataset_id, file_path)
    print(f"  [{time.time()-t0:.1f}s]")
    print(_short(result))


def cmd_download(use_aurum: bool):
    print("  Enter files to download. Empty dataset_id to stop.")
    files = []
    while True:
        d = input("    dataset_id: ").strip()
        if not d:
            break
        f = input("    file_path: ").strip()
        if f:
            files.append({"dataset_id": d, "file_path": f})
    if not files:
        print("  [!] Nothing to download.")
        return
    t0 = time.time()
    result = agent_tools.download(files)
    print(f"  [{time.time()-t0:.1f}s]")
    print(_short(result))


def cmd_execute_code(use_aurum: bool):
    print("  Enter Python code. Type END on its own line to run.")
    lines = []
    while True:
        line = input("  >>> ")
        if line.strip() == "END":
            break
        lines.append(line)
    code = "\n".join(lines)
    if not code.strip():
        print("  [!] No code entered.")
        return
    t0 = time.time()
    result = agent_tools.execute_code(code)
    print(f"  [{time.time()-t0:.1f}s]")
    # execute_code returns stdout/stderr as strings — print them directly
    if "output" in result:
        print(result["output"])
    if "error" in result:
        print(f"  [ERROR] {result['error']}")
    other = {k: v for k, v in result.items() if k not in ("output", "error")}
    if other:
        _pp(other)


def cmd_sandbox_info(use_aurum: bool):
    _pp(agent_tools.get_sandbox_info())


# Aurum tools
def cmd_search_value(use_aurum: bool):
    if not use_aurum:
        print("  [!] Aurum not enabled. Run with --use-aurum.")
        return
    from evaluation.tools.aurum_tools import search_value
    query = input("  query: ").strip()
    top_k_raw = input("  top_k [10]: ").strip()
    top_k = int(top_k_raw) if top_k_raw.isdigit() else 10
    t0 = time.time()
    result = search_value(query, top_k=top_k)
    print(f"  [{time.time()-t0:.1f}s]")
    print(_short(result))


def cmd_search_field(use_aurum: bool):
    if not use_aurum:
        print("  [!] Aurum not enabled. Run with --use-aurum.")
        return
    from evaluation.tools.aurum_tools import search_field
    query = input("  query: ").strip()
    top_k_raw = input("  top_k [10]: ").strip()
    top_k = int(top_k_raw) if top_k_raw.isdigit() else 10
    t0 = time.time()
    result = search_field(query, top_k=top_k)
    print(f"  [{time.time()-t0:.1f}s]")
    print(_short(result))


def cmd_neighbor(use_aurum: bool):
    if not use_aurum:
        print("  [!] Aurum not enabled. Run with --use-aurum.")
        return
    from evaluation.tools.aurum_tools import neighbor
    inp = input("  input (table or column id): ").strip()
    relation = input("  relation [pkfk/content/schema, default pkfk]: ").strip() or "pkfk"
    top_k_raw = input("  top_k [10]: ").strip()
    top_k = int(top_k_raw) if top_k_raw.isdigit() else 10
    t0 = time.time()
    result = neighbor(inp, relation=relation, top_k=top_k)
    print(f"  [{time.time()-t0:.1f}s]")
    print(_short(result))


# ---------------------------------------------------------------------------
# Command dispatch
# ---------------------------------------------------------------------------

BASE_COMMANDS = {
    "search":         ("search datasets by prefix",              cmd_search),
    "kw":             ("search_keyword — semantic search",       cmd_search_keyword),
    "ls":             ("list_files in dataset(s)",               cmd_list_files),
    "inspect":        ("inspect_file structure/sample",          cmd_inspect_file),
    "dl":             ("download file(s) to sandbox",            cmd_download),
    "run":            ("execute_code in sandbox",                cmd_execute_code),
    "sandbox":        ("show sandbox info / downloaded files",   cmd_sandbox_info),
}

AURUM_COMMANDS = {
    "sv":             ("search_value — find columns by value",   cmd_search_value),
    "sf":             ("search_field — find columns by name",    cmd_search_field),
    "nb":             ("neighbor — find related tables",         cmd_neighbor),
}


def print_help(use_aurum: bool):
    print("\nAvailable commands:")
    for cmd, (desc, _) in BASE_COMMANDS.items():
        print(f"  {cmd:<12}  {desc}")
    if use_aurum:
        for cmd, (desc, _) in AURUM_COMMANDS.items():
            print(f"  {cmd:<12}  {desc}  [aurum]")
    print(f"  {'submit':<12}  submit your final answer")
    print(f"  {'skip':<12}  skip this task (reveal answer)")
    print(f"  {'help':<12}  show this help")
    print(f"  {'quit':<12}  exit\n")


# ---------------------------------------------------------------------------
# Task loading
# ---------------------------------------------------------------------------

def load_task(task_file: str) -> dict:
    with open(task_file) as f:
        return json.load(f)


def pick_random_task() -> str:
    tasks = list(Path("tasks").rglob("*.json"))
    if not tasks:
        sys.exit("No tasks found in tasks/")
    return str(random.choice(tasks))


# ---------------------------------------------------------------------------
# Main REPL
# ---------------------------------------------------------------------------

def run_repl(question: str, answer: str | None, use_aurum: bool):
    # Set up a fresh sandbox for this session
    sandbox = Path(_ROOT) / ".sandbox" / f"human_{int(time.time())}"
    agent_tools.set_sandbox_dir(sandbox)

    all_commands = dict(BASE_COMMANDS)
    if use_aurum:
        all_commands.update(AURUM_COMMANDS)
        print("[aurum] Loading index... ", end="", flush=True)
        from evaluation.tools.aurum_tools import _get_aurum_agent
        _get_aurum_agent()
        print("ready.")

    _banner(f"QUESTION:\n{question}")
    print_help(use_aurum)

    start = time.time()

    while True:
        try:
            raw = input("\n> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n[interrupted]")
            break

        if not raw:
            continue

        cmd = raw.lower()

        if cmd in ("quit", "exit", "q"):
            break

        elif cmd in ("help", "h", "?"):
            print_help(use_aurum)

        elif cmd == "skip":
            if answer:
                print(f"\n  Correct answer: {answer}")
            else:
                print("  No answer available for this task.")
            break

        elif cmd == "submit":
            ans = input("  Your answer: ").strip()
            elapsed = time.time() - start
            print(f"\n  Submitted: {ans}")
            print(f"  Time: {elapsed:.1f}s")
            if answer:
                import re
                norm = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())
                correct = norm(ans) == norm(answer)
                print(f"  Correct answer: {answer}")
                print(f"  Result: {'✓ CORRECT' if correct else '✗ WRONG'}")
            break

        elif cmd in all_commands:
            _, fn = all_commands[cmd]
            try:
                fn(use_aurum)
            except Exception as e:
                print(f"  [ERROR] {e}")

        else:
            print(f"  Unknown command '{cmd}'. Type 'help' for options.")

    # Cleanup sandbox
    try:
        import shutil
        shutil.rmtree(sandbox, ignore_errors=True)
    except Exception:
        pass


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Run a benchmark task as a human agent")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--task", help="Path to a task JSON file")
    group.add_argument("--question", help="Ad-hoc question to answer")
    parser.add_argument("--use-aurum", action="store_true", help="Enable Aurum discovery tools")
    args = parser.parse_args()

    if args.question:
        question = args.question
        answer = None
    else:
        task_file = args.task or pick_random_task()
        print(f"Task file: {task_file}")
        task = load_task(task_file)
        question = task["question"]
        answer = task.get("answer")

    run_repl(question, answer, use_aurum=args.use_aurum)


if __name__ == "__main__":
    main()
