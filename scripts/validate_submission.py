#!/usr/bin/env python3
"""
🛡️ GitHub Achievements Arena — 5-Gate Automated Moderation & Schema Validator
==============================================================================
Validates contributor profiles (`contributors/*.json`) and community engineering
lessons (`lessons/community/*.json`) for schema compliance, ownership integrity,
and DLP/anti-spam safety.
"""

import argparse
import json
import pathlib
import re
import sys

FORBIDDEN_PATTERNS = [
    (re.compile(r"gh[pousr]_[A-Za-z0-9_]{20,}"), "Potential leaked GitHub token"),
    (re.compile(r"sk-[A-Za-z0-9]{20,}"), "Potential leaked OpenAI/API secret key"),
    (re.compile(r"AIza[0-9A-Za-z\-_]{30,}"), "Potential leaked Google API key"),
    (re.compile(r"<script\b", re.IGNORECASE), "HTML <script> tag injection"),
    (re.compile(r"javascript:", re.IGNORECASE), "javascript: URI injection"),
    (re.compile(r"https?://(?:bit\.ly|tinyurl\.com|t\.co)/", re.IGNORECASE), "Disallowed URL shortener"),
]


def scan_dlp_and_spam(text: str, filepath: str) -> list[str]:
    errors = []
    if len(text.encode("utf-8")) > 15360:
        errors.append(f"{filepath}: File size exceeds 15 KB limit.")
    for rx, reason in FORBIDDEN_PATTERNS:
        if rx.search(text):
            errors.append(f"{filepath}: Blocked by DLP/Anti-Spam filter ({reason}).")
    return errors


def validate_contributor_file(path: pathlib.Path, expected_author: str | None = None) -> list[str]:
    errors = []
    raw = path.read_text(encoding="utf-8")
    errors.extend(scan_dlp_and_spam(raw, str(path)))
    try:
        data = json.loads(raw)
    except Exception as exc:
        return [f"{path}: Invalid JSON syntax ({exc})."]

    if not isinstance(data, dict):
        return [f"{path}: Root JSON value must be an object."]

    username = str(data.get("username", "")).strip()
    if not username:
        errors.append(f"{path}: Missing required string field 'username'.")
    if path.stem.lower() != username.lower():
        errors.append(f"{path}: Filename '{path.name}' must match username '{username}.json'.")
    if expected_author and expected_author.lower() not in {username.lower(), "khoap1220-hue"}:
        errors.append(f"{path}: PR author '@{expected_author}' cannot modify '@{username}'s profile.")

    badges = data.get("target_badges")
    if not isinstance(badges, list) or not badges:
        errors.append(f"{path}: 'target_badges' must be a non-empty list of strings.")
    return errors


def validate_lesson_file(path: pathlib.Path, expected_author: str | None = None) -> list[str]:
    errors = []
    raw = path.read_text(encoding="utf-8")
    errors.extend(scan_dlp_and_spam(raw, str(path)))
    try:
        data = json.loads(raw)
    except Exception as exc:
        return [f"{path}: Invalid JSON syntax ({exc})."]

    if not isinstance(data, dict):
        return [f"{path}: Root JSON value must be an object."]

    required_fields = ["id", "author", "title", "category", "language", "problem", "solution"]
    for req in required_fields:
        val = str(data.get(req, "")).strip()
        if not val:
            errors.append(f"{path}: Missing required field '{req}'.")
        elif req in {"title", "problem", "solution"} and len(val) < 15:
            errors.append(f"{path}: Field '{req}' must be at least 15 characters long.")

    author = str(data.get("author", "")).strip()
    if author and not path.stem.lower().startswith(author.lower()):
        errors.append(f"{path}: Lesson filename '{path.name}' must start with author username '{author}-...'.")
    if expected_author and expected_author.lower() not in {author.lower(), "khoap1220-hue"}:
        errors.append(f"{path}: PR author '@{expected_author}' cannot modify a lesson owned by '@{author}'.")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Arena JSON submissions")
    parser.add_argument("--author", default=None, help="GitHub login of PR author for ownership check")
    parser.add_argument("files", nargs="*", help="Specific files to validate (defaults to all JSON files)")
    args = parser.parse_args()

    root = pathlib.Path(__file__).resolve().parent.parent
    targets = [pathlib.Path(f) for f in args.files] if args.files else (
        list((root / "contributors").glob("*.json")) + list((root / "lessons" / "community").glob("*.json"))
    )

    all_errors: list[str] = []
    for p in targets:
        if not p.exists():
            continue
        rel = p.resolve().relative_to(root) if p.is_absolute() else p
        parts = rel.parts
        if len(parts) == 2 and parts[0] == "contributors" and p.suffix == ".json":
            all_errors.extend(validate_contributor_file(p, args.author))
        elif len(parts) == 3 and parts[0] == "lessons" and parts[1] == "community" and p.suffix == ".json":
            all_errors.extend(validate_lesson_file(p, args.author))

    if all_errors:
        print("❌ Moderation Validation Failed:")
        for e in all_errors:
            print("  -", e)
        return 1

    print(f"✅ All {len(targets)} file(s) passed 5-Gate Schema, Ownership & DLP Moderation!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
