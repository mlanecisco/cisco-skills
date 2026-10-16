"""Local publishing simulation. No network requests or real macro representation."""

import argparse
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--state", type=Path, required=True)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("get")
    update = commands.add_parser("update")
    update.add_argument("--expected-version", type=int, required=True)
    update.add_argument("--body", type=Path, required=True)
    args = parser.parse_args()
    state = json.loads(args.state.read_text())
    if args.command == "get":
        if not state.get("read_available", True):
            print("Synthetic page read unavailable")
            return 69
        view = {key: state[key] for key in ("site", "page_id", "version", "published", "restrictions", "draft_available")}
        view["draft"] = state["draft"] if state["draft_available"] else None
        print(json.dumps(view))
        return 0
    if args.expected_version != state["version"]:
        print("Synthetic version conflict; no write")
        return 73
    body = json.loads(args.body.read_text())
    state["published"] = body
    state["draft"] = body
    state["version"] += 1
    state["writes"] += 1
    outcome = state.pop("next_response", "success")
    if outcome == "lost-and-unreadable":
        state["read_available"] = False
    args.state.write_text(json.dumps(state, indent=2) + "\n")
    if outcome in {"lost", "lost-and-unreadable"}:
        print("Synthetic connection lost; update outcome not returned")
        return 75
    print("Synthetic update accepted; rendering not simulated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
