# 🧠 Community Engineering Lessons Repository (`Moderated Global Contributions`)

Welcome to the **Moderated Community Lessons Vault**!
Here, developers from around the world can contribute real-world lessons learned from code reviews, debugging sessions, system design, or open-source contributions — while earning **`🦈 Pull Shark`** and **`👯 Pair Extraordinaire`**!

---

## 🛡️ How Our 5-Gate Automated Moderation Works

To keep this repository high-quality, spam-free, and genuinely helpful for new developers entering the job market, every Pull Request goes through `.github/workflows/auto-merge-arena.yml` and `scripts/validate_submission.py`:

| Gate | Moderation Check | What Is Allowed (`✅ Pass`) | What Is Blocked (`❌ Rejected`) |
| :---: | :--- | :--- | :--- |
| **Gate 1** | **Ownership & Path Quarantine** | Creating/updating your own `contributors/<you>.json`, `lessons/community/<you>-<slug>.json`, or appending 1 row to `HALL_OF_FAME.md`. | Modifying or deleting another user's JSON file, deleting existing rows in `HALL_OF_FAME.md`, or editing `.github/` workflows. |
| **Gate 2** | **Strict JSON Schema Validation** | Valid UTF-8 JSON matching the required fields and length constraints (`20..2,000` chars). | Malformed JSON, empty fields, or oversized files (`> 15 KB`). |
| **Gate 3** | **Anti-Spam, DLP & Security Scan** | Clean technical explanations, code snippets, and valid GitHub URLs. | Leaked API keys (`ghp_`, `sk-`), phishing/shortener links (`bit.ly`), `<script>` injection, or promotional spam. |
| **Gate 4** | **Star Verification (`⭐`)** | Contributor has clicked **`⭐ Star`** on `khoap1220-hue/github-achievements-arena`. | Unstarred accounts (Bot pauses and asks you to click `⭐ Star` first). |
| **Gate 5** | **Tiered Editorial Governance** | • **Tier A (`contributors/*.json`, `lessons/community/*.json`):** Auto-approved & merged in 10s when Gates 1–4 pass!<br>• **Tier B (`docs/*.md`, `README.md`, `web/*`):** Automated checks run first, then labeled `needs-maintainer-review` for `@khoap1220-hue` approval! | Unverified edits to core system files without maintainer sign-off. |

---

## 📝 JSON Schema for Submitting a Community Lesson (`lessons/community/<your-username>-<slug>.json`)

Create a file named `lessons/community/<your-username>-<short-topic>.json` with the following structure:

```json
{
  "id": "LESSON-khoap1220-hue-atomic-writes",
  "author": "khoap1220-hue",
  "title": "Use Atomic Tempfile + os.replace() Instead of Direct File Overwrites",
  "category": "Concurrency & Reliability",
  "language": "Python",
  "problem": "Writing directly to state.json with write_text() can leave a truncated or 0-byte file if the process crashes or loses power mid-write.",
  "solution": "Write the full payload to a temporary file in the same directory, flush to disk, and atomically swap it into place with os.replace().",
  "code_example": "with tempfile.NamedTemporaryFile('w', dir=parent, delete=False) as f:\n    f.write(payload)\n    tmp_name = f.name\nos.replace(tmp_name, target_path)",
  "created_at": "2026-10-29"
}
```
