# 🛡️ Contributing & Automated 5-Gate Moderation Policy

Thank you for contributing to **GitHub Achievements & Career Launchpad Arena**!
To keep this project safe, educational, and welcoming for developers worldwide, all contributions are governed by our **2-Tier Automated Moderation System (`.github/workflows/auto-merge-arena.yml`)**.

---

## 🚦 Two Contribution Tiers (`Instant Auto-Merge` vs `Maintainer Editorial Review`)

| Tier | Allowed File Paths | Moderation Flow | Merge Speed |
| :---: | :--- | :--- | :---: |
| **🟢 Tier A (`Self-Service Arena & Community Lessons`)** | • `contributors/<your-username>.json`<br>• `lessons/community/<your-username>-<slug>.json`<br>• Appending 1 row to `HALL_OF_FAME.md` | Automatically audited by our **5-Gate Moderation Bot** (Ownership Lock, Anti-Deletion Guard, JSON Schema, DLP/Anti-Spam, and ⭐ Star Check). | **⚡ 10 Seconds (Auto-Merged by Bot)** |
| **🟡 Tier B (`Core Playbooks, Web Studio & Scripts`)** | • `docs/*.md`<br>• `README.md`<br>• `web/*`<br>• `scripts/*` | Passes automated DLP & syntax checks first, then labeled `needs-maintainer-review` for editorial sign-off by maintainer **`@khoap1220-hue`**. | **👨‍💻 Maintainer Reviewed** |
| **🔴 Blocked (`Restricted Paths`)** | • `.github/workflows/*`<br>• Deleting existing files or editing another user's JSON file | Automatically blocked by Gate 1 (`Ownership & Workflow Security Lock`). | **🚫 Blocked** |

---

## 🧪 Running the Moderation Check Locally Before Pushing

You can run the exact same validator locally using Python 3:

```bash
python scripts/validate_submission.py --author your-github-username
```
