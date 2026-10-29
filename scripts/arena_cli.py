#!/usr/bin/env python3
"""
🏆 GitHub Achievements Arena — 1-Command Global Unlocker CLI (scripts/arena_cli.py)
===================================================================================
Unlock the entire GitHub Earned Achievements collection automatically using the `gh` CLI!

Usage:
    python scripts/arena_cli.py --all
    python scripts/arena_cli.py --pull-shark --count 2
    python scripts/arena_cli.py --quickdraw
    python scripts/arena_cli.py --yolo
"""

import argparse
import base64
import datetime
import json
import subprocess
import sys
import time

ARENA_REPO = "khoap1220-hue/github-achievements-arena"
COAUTHOR_TRAILER = "Co-authored-by: Khoa Phan <233728558+khoap1220-hue@users.noreply.github.com>"


def run_gh(args: list[str], input_data: str | None = None) -> str:
    res = subprocess.run(
        ["gh"] + args,
        input=input_data,
        text=True,
        capture_output=True,
        encoding="utf-8",
    )
    if res.returncode != 0:
        raise RuntimeError(f"gh {' '.join(args)} failed: {res.stderr.strip()}")
    return res.stdout.strip()


def get_current_user() -> dict:
    return json.loads(run_gh(["api", "user"]))


def ensure_starred() -> None:
    print(f"⭐ Starring {ARENA_REPO} to activate the 10-Second Auto-Merge Gate...")
    run_gh(["api", "-X", "PUT", f"/user/starred/{ARENA_REPO}"])
    print("✅ Starred!")


def unlock_quickdraw() -> None:
    print("⚡ Unlocking Quickdraw (opening & closing an issue within 5 seconds)...")
    iss = json.loads(
        run_gh(
            [
                "api",
                "-X",
                "POST",
                f"/repos/{ARENA_REPO}/issues",
                "-f",
                "title=[Quickdraw] ⚡ Automated CLI Quickdraw Unlock",
                "-f",
                "body=Unlocking ⚡ Quickdraw via `scripts/arena_cli.py`!",
            ]
        )
    )
    num = iss["number"]
    time.sleep(2)
    run_gh(
        [
            "api",
            "-X",
            "PATCH",
            f"/repos/{ARENA_REPO}/issues/{num}",
            "-f",
            "state=closed",
            "-f",
            "state_reason=completed",
        ]
    )
    print(f"✅ Quickdraw unlocked via Issue #{num}: {iss['html_url']}")


def unlock_pull_shark_and_pair(user: dict, count: int = 1) -> None:
    login = user["login"]
    print(f"🦈👯 Unlocking Pull Shark & Pair Extraordinaire ({count} PR(s)) for @{login}...")
    # Ensure fork exists
    run_gh(["api", "-X", "POST", f"/repos/{ARENA_REPO}/forks"])
    time.sleep(3)

    for i in range(1, count + 1):
        # Sync fork with upstream main
        try:
            run_gh(["api", "-X", "POST", f"/repos/{login}/github-achievements-arena/merge-upstream", "-f", "branch=main"])
        except Exception:
            pass

        main_ref = json.loads(run_gh(["api", f"/repos/{login}/github-achievements-arena/git/ref/heads/main"]))
        base_sha = main_ref["object"]["sha"]
        branch_name = f"feat/arena-{login}-{int(time.time())}-{i}"

        run_gh(
            [
                "api",
                "-X",
                "POST",
                f"/repos/{login}/github-achievements-arena/git/refs",
                "-f",
                f"ref=refs/heads/{branch_name}",
                "-f",
                f"sha={base_sha}",
            ]
        )

        # Check if contributors/<login>.json already exists
        existing_sha = None
        runs = i
        try:
            existing_file = json.loads(
                run_gh(["api", f"/repos/{login}/github-achievements-arena/contents/contributors/{login}.json?ref={branch_name}"])
            )
            existing_sha = existing_file.get("sha")
            old_data = json.loads(base64.b64decode(existing_file["content"]).decode("utf-8"))
            runs = int(old_data.get("arena_prs_count", 0)) + 1
        except Exception:
            pass

        payload_json = json.dumps(
            {
                "username": login,
                "name": user.get("name") or login,
                "target_badges": ["Pull Shark", "Pair Extraordinaire", "Quickdraw", "Galaxy Brain", "YOLO"],
                "arena_prs_count": runs,
                "updated_at": datetime.date.today().isoformat(),
            },
            indent=2,
        ) + "\n"

        commit_msg = f"feat(arena): update @{login} contributor milestone #{runs}\n\n{COAUTHOR_TRAILER}"
        put_args = [
            "api",
            "-X",
            "PUT",
            f"/repos/{login}/github-achievements-arena/contents/contributors/{login}.json",
            "-f",
            f"message={commit_msg}",
            "-f",
            f"content={base64.b64encode(payload_json.encode('utf-8')).decode('ascii')}",
            "-f",
            f"branch={branch_name}",
        ]
        if existing_sha:
            put_args.extend(["-f", f"sha={existing_sha}"])
        run_gh(put_args)

        pr = json.loads(
            run_gh(
                [
                    "api",
                    "-X",
                    "POST",
                    f"/repos/{ARENA_REPO}/pulls",
                    "-f",
                    f"title=feat(arena): @{login} achievement milestone #{runs}",
                    "-f",
                    f"head={login}:{branch_name}",
                    "-f",
                    "base=main",
                    "-f",
                    f"body=Automated Arena PR #{runs} for @{login}.\n\n{COAUTHOR_TRAILER}",
                ]
            )
        )
        print(f"🚀 Opened PR #{pr['number']}: {pr['html_url']} — waiting 15s for Arena Bot to auto-merge...")
        time.sleep(16)


def main() -> None:
    parser = argparse.ArgumentParser(description="GitHub Achievements Arena 1-Command Unlocker")
    parser.add_argument("--all", action="store_true", help="Unlock Quickdraw + Pull Shark + Pair Extraordinaire")
    parser.add_argument("--quickdraw", action="store_true", help="Unlock Quickdraw badge")
    parser.add_argument("--pull-shark", action="store_true", help="Unlock Pull Shark & Pair Extraordinaire")
    parser.add_argument("--count", type=int, default=2, help="Number of PRs to open & auto-merge (default: 2)")
    args = parser.parse_args()

    user = get_current_user()
    ensure_starred()

    if args.all or args.quickdraw:
        unlock_quickdraw()
    if args.all or args.pull_shark:
        unlock_pull_shark_and_pair(user, count=args.count)

    print("\n🎉 Done! Check your badges at: https://github.com/" + user["login"] + "?tab=achievements")


if __name__ == "__main__":
    main()
