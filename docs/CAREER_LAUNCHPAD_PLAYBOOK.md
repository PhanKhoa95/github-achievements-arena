# 🎓 New Developer Career Launchpad Playbook (`From First PR to Paid Open-Source`)

Welcome! If you are a student, bootcamp graduate, self-taught programmer, or junior developer entering the software engineering market, this playbook shows you how to turn your **GitHub Profile** into a **Recruiter & Bounty Magnet**.

---

## 🧭 Stage 1: The 30-Second Recruiter GitHub Test

When a hiring manager or open-source maintainer clicks your GitHub link on your resume, they look at **5 signals in the first 30 seconds**:

| Signal | What Recruiters Look For | How to Fix It Today in 5 Minutes |
| :--- | :--- | :--- |
| **1. Profile README (`username/username`)** | A clean, scannable introduction showing your core tech stack, featured projects, and contact info. | Open a **[🎓 Free 100-Point Career Audit Issue](https://github.com/khoap1220-hue/github-achievements-arena/issues/new?template=03-career-profile-audit.yml)** in this repo — our Bot will generate a customized `README.md` for your exact profile in 15 seconds! |
| **2. Earned Achievements (`Badges`)** | Proof that you know how to collaborate via Pull Requests (`🦈 Pull Shark`), pair program (`👯 Pair Extraordinaire`), and help peers in technical discussions (`🧠 Galaxy Brain`). | Use our **10-Second Auto-Merge Arena** and **Auto-Accept Q&A Discussions** to unlock all core badges. |
| **3. GPG `Verified` Commits** | The green **`Verified`** pill next to your commits proves cryptographic authorship and security awareness. | Enable GPG/SSH commit signing in `git config --global commit.gpgsign true` or commit via GitHub's GraphQL/Web flow. |
| **4. Real-World PR Etiquette** | Knowing the difference between **Code-First** vs **Assign-First** repositories and reading CI logs before asking for review. | Practice in our [`sandbox/`](../sandbox/README.md) directory and read Section 2 below! |
| **5. Pinned Repositories (Top 6)** | 3–6 repositories that have a clear **1-sentence description**, **Topics/Tags**, a **Live Demo or Screenshot**, and **Tests**. | Never leave a pinned repository with an empty description or default boilerplate README! |

---

## 🛡️ Stage 2: 5 Golden Rules of Real-World Open-Source Contributions

Before submitting Pull Requests to major open-source projects (like `tldr-pages/tldr`, `firstcontributions`, or paid bounty repositories), follow these **5 Golden Rules**:

1. **Always Check `CONTRIBUTING.md` for `Assign-First` vs `Code-First`:**
   - **Code-First (e.g., Algora bounties, docs fixes):** You can open a Pull Request directly referencing `Fixes #<issue>`.
   - **Assign-First (e.g., Drips Stellar Wave, OnlyDust):** You **must** post a short, 3-step technical implementation plan on the Issue and wait until a maintainer assigns you (`assignees`) before opening a PR.
2. **Never Spam or Nag Maintainers:**
   - Once your PR is open and all CI checks (`🟢`) are green, **never** comment `"Any update?"` or `"Please merge"`. Maintainers review asynchronously across timezones.
3. **Always Run Linters & Tests Locally First:**
   - Inspect `.github/workflows/*.yml` in the target repository to see the exact test commands (`pytest`, `npm test`, `cargo test`, `go test ./...`) that CI will run.
4. **One Issue = One Focused Pull Request:**
   - Do not bundle unrelated formatting changes or extra files into your PR. Keep the diff minimal and surgical.
5. **Check for Existing Competing PRs:**
   - Before spending hours coding an issue, check the issue timeline to make sure another developer hasn't already submitted an open PR for it.

---

## 💰 Stage 3: Where to Find Paid Open-Source Internships, Grants & Bounties

Once you have unlocked your badges and practiced the workflow in this Arena, graduate to these global programs that pay developers for open-source contributions:

| Program / Platform | Compensation Type | Best For | Website |
| :--- | :--- | :--- | :--- |
| **Algora Bounties** | `$50 – $2,500+ USD` per merged PR *(Escrow)* | Rust, TypeScript, Go, Python developers | `https://console.algora.io` |
| **Drips Stellar Wave** | `$75,000 USDC` per Wave cycle | Rust, Soroban Smart Contracts, Go, TypeScript | `https://www.drips.network/wave/stellar` |
| **Google Summer of Code (GSoC)** | `$1,500 – $6,600 USD` stipend | University students & open-source beginners | `https://summerofcode.withgoogle.com` |
| **LFX Mentorship (Linux Foundation)** | `$3,000 – $6,600 USD` stipend | Cloud-native, Linux, Kubernetes, Security | `https://mentorship.lfx.linuxfoundation.org` |
| **First Contributions & TLDR Pages** | High-Star Portfolio Credibility (`45k–52k ⭐`) | Your very first external Pull Request | `https://github.com/tldr-pages/tldr` |
