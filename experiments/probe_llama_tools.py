"""
Probe Llama 3.3-70B tool call format via raw Bedrock converse_stream.

Usage:
    python experiments/probe_llama_tools.py [--tool-choice auto|any]

Reads BEDROCK_LLAMA_ARN from .env / environment.
Prints each raw stream chunk so you can see whether Llama emits:
  - contentBlockStart.start.toolUse  -> native tool_use (Strands will dispatch it)
  - contentBlockDelta.delta.text     -> plain-text JSON (Strands ignores it)
"""

import argparse
import json
import os
import sys

from dotenv import load_dotenv

load_dotenv()

import boto3


def probe(tool_choice_mode: str) -> None:
    model_arn = os.environ.get("PROBE_MODEL_ID") or os.environ.get("BEDROCK_LLAMA_ARN")
    if not model_arn:
        print("ERROR: BEDROCK_LLAMA_ARN not set in environment / .env", file=sys.stderr)
        sys.exit(1)

    region = model_arn.split(":")[3] if model_arn.startswith("arn:aws:bedrock:") else "us-east-1"
    client = boto3.client("bedrock-runtime", region_name=region)

    tool_choice: dict
    if tool_choice_mode == "any":
        tool_choice = {"any": {}}
    elif tool_choice_mode == "auto":
        tool_choice = {"auto": {}}
    else:
        print(f"Unknown tool_choice mode: {tool_choice_mode}", file=sys.stderr)
        sys.exit(1)

    tool_config = {
        "tools": [
            {
                "toolSpec": {
                    "name": "search",
                    "description": "Search for information in a data lake",
                    "inputSchema": {
                        "json": {
                            "type": "object",
                            "properties": {
                                "query": {"type": "string", "description": "Search query"}
                            },
                            "required": ["query"],
                        }
                    },
                }
            }
        ],
        "toolChoice": tool_choice,
    }

    print(f"=== Probing {model_arn}")
    print(f"=== toolChoice: {tool_choice}")
    print("=== Sending: 'Search for the capital of France'\n")

    # First try non-streaming (converse), since Llama doesn't support streaming + tools
    print("--- Trying non-streaming (converse) ---")
    try:
        resp_ns = client.converse(
            modelId=model_arn,
            messages=[
                {
                    "role": "user",
                    "content": [{"text": "Search for the capital of France"}],
                }
            ],
            toolConfig=tool_config,
        )
        print(json.dumps(resp_ns, default=str))
        content = resp_ns.get("output", {}).get("message", {}).get("content", [])
        has_tool_use = any("toolUse" in block for block in content)
        stop_reason = resp_ns.get("stopReason", "?")
        print(f"\n=== NON-STREAMING SUMMARY ===")
        print(f"stopReason: {stop_reason}")
        if has_tool_use:
            print("RESULT: Native toolUse blocks in response — non-streaming works!")
        else:
            print("RESULT: No toolUse blocks — even non-streaming doesn't trigger tool calls.")
    except Exception as e:
        print(f"Non-streaming also failed: {e}")

    print("\n--- Trying streaming (converse_stream) ---")
    try:
        resp = client.converse_stream(
            modelId=model_arn,
            messages=[
                {
                    "role": "user",
                    "content": [{"text": "Search for the capital of France"}],
                }
            ],
            toolConfig=tool_config,
        )

        has_tool_use_event = False
        has_text_event = False

        for chunk in resp["stream"]:
            print(json.dumps(chunk, default=str))

            if "contentBlockStart" in chunk:
                start = chunk["contentBlockStart"].get("start", {})
                if "toolUse" in start:
                    has_tool_use_event = True

            if "contentBlockDelta" in chunk:
                delta = chunk["contentBlockDelta"].get("delta", {})
                if "text" in delta:
                    has_text_event = True

        print("\n=== STREAMING SUMMARY ===")
        if has_tool_use_event:
            print("RESULT: Native toolUse blocks detected — streaming works!")
        elif has_text_event:
            print("RESULT: Only text deltas — Llama emits tool calls as plain text in streaming mode.")
        else:
            print("RESULT: No content detected in streaming mode.")
    except Exception as e:
        print(f"Streaming failed: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--tool-choice",
        choices=["auto", "any"],
        default="auto",
        help="toolChoice mode to test (default: auto)",
    )
    args = parser.parse_args()
    probe(args.tool_choice)
