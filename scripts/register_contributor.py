#!/usr/bin/env python3
"""Helper CLI to generate or update your contributor entry in GitHub Achievements Arena."""

import argparse
import datetime
import json
import pathlib


def main() -> None:
    parser = argparse.ArgumentParser(description="Register contributor in GitHub Achievements Arena")
    parser.add_argument("--username", required=True, help="Your GitHub username")
    parser.add_argument("--name", default="", help="Your display name")
    parser.add_argument("--badge", default="Pull Shark, Pair Extraordinaire", help="Target badges")
    args = parser.parse_args()

    root = pathlib.Path(__file__).resolve().parent.parent
    contrib_dir = root / "contributors"
    contrib_dir.mkdir(exist_ok=True)

    today = datetime.date.today().isoformat()
    profile_path = contrib_dir / f"{args.username}.json"
    existing = {}
    if profile_path.exists():
        try:
            existing = json.loads(profile_path.read_text(encoding="utf-8"))
        except Exception:
            existing = {}

    runs = int(existing.get("arena_prs_count", 0)) + 1
    data = {
        "username": args.username,
        "name": args.name or args.username,
        "target_badges": [b.strip() for b in args.badge.split(",") if b.strip()],
        "arena_prs_count": runs,
        "updated_at": today,
    }
    profile_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(f"Updated {profile_path} (arena_prs_count={runs})")


if __name__ == "__main__":
    main()
