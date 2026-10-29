# 📚 25 Battle-Tested Open-Source & Code Review Lessons (`Distilled from Real Maintainer Reviews`)

> **Why this handbook exists:** Most new developers get their first open-source Pull Requests closed not because they can't code, but because they hit **unwritten repository governance rules** or **production edge cases** flagged by senior maintainers and AI review bots (`@coderabbitai`, `@sourcery-ai`, `@greptile-apps`).
>
> Below are **25 distilled engineering lessons** (6 PR Survival Post-Mortem Rules + 19 Production Code Review Patterns) harvested from real open-source contributions across Rust, Go, TypeScript, and Python ecosystems.

---

## 🛑 Part 1: The 6 Post-Mortem PR Survival Rules (`Why PRs Get Closed & How to Prevent It`)

| Rule ID | Common Newbie Mistake (`Root Cause`) | What Happens on Real Repositories | Mandatory Pre-Flight Gate (`The Fix`) |
| :---: | :--- | :--- | :--- |
| **`PM-01`** | **Coding on an `Assign-First` repo without assignment** | Repos using Drips Stellar Wave, OnlyDust, or `.github/workflows/require-assignment.yml` automatically close unassigned PRs within seconds. | Strip markdown formatting (`*`, `_`) and scan `CONTRIBUTING.md` + `.github/workflows/*.yml` first. If `Assign-First`, post a 3-step technical plan on the Issue and wait until your username appears in `issue.assignees`. |
| **`PM-02`** | **Batch-flooding multiple PRs to the same repository** | Opening 3–5 PRs in 10 minutes to one repo triggers maintainer fatigue and spam filters, causing all PRs to be closed. | **Strict `1 Repo = 1 Open PR` Rule:** Submit your best single PR first. Wait until maintainers review or merge it before opening a second PR on that repository. |
| **`PM-03`** | **Contributing to dormant / abandoned repositories** | You spend days writing code for a repository whose maintainers left a year ago (`pushed_at > 90 days`), so your PR sits forever. | **90-Day Commit Velocity Gate:** Always verify the repository has merged commits within the last 90 days and has no maintainer cancellation notice on the issue. |
| **`PM-04`** | **Opening a duplicate PR on an already-claimed issue** | Another contributor already opened an active PR linked to `#issue` hours earlier; maintainers merge the first clean PR. | Query the issue timeline (`CROSS_REFERENCED_EVENT`) before coding. Never start an issue that already has an open competing PR. |
| **`PM-05`** | **Editing legacy/deprecated directories** | Repos undergoing migration (e.g., `apps/desktop` -> `apps/desktop-gpui`, or `old-architecture` -> `main`) reject PRs touching legacy folders. | Inspect the 10 most recent merged commits on the default branch to confirm which module directory is actively maintained. |
| **`PM-06`** | **Publicly nagging maintainers or discussing bounty money** | Commenting `"Any update?"`, `"Please merge"`, or `"When will the bounty be paid?"` alienates maintainers immediately. | **100% Pure Engineering Etiquette:** Never post unsolicited follow-ups or mention payouts (`$`) on GitHub. Let your green CI checks (`🟢`) and GPG `Verified` commits speak for themselves. |

---

## 🛡️ Part 2: 19 Production Code Review Patterns (`REV-LESSON-01..19`)

### 🔐 Category A: Security, Auth & Input Hygiene (`REV-01..05`)

| ID | Pattern Name | Anti-Pattern (`Rejected in Review ❌`) | Senior Production Pattern (`Approved ✅`) |
| :---: | :--- | :--- | :--- |
| **`REV-01`** | **Constant-Time Secret Comparison** | `if api_key == expected_key:` *(vulnerable to timing side-channel attacks)* | Use `hmac.compare_digest(a, b)` (Python), `crypto.timingSafeEqual` (Node.js), or `subtle::ConstantTimeEq` (Rust). |
| **`REV-02`** | **SSRF & IP-Literal Validation** | Checking `url.startswith("https://")` without blocking internal IPs (`127.0.0.1`, `169.254.169.254`) | Parse hostname and reject private/loopback/link-local IPs (`ipaddress.ip_address(host).is_global`). |
| **`REV-03`** | **Path Traversal Containment** | `open(os.path.join(base_dir, user_filename))` *(allows `../../etc/passwd`)* | Resolve canonical path via `Path(base_dir, user_path).resolve()` and assert `.is_relative_to(base_dir)`. |
| **`REV-04`** | **Secret Redaction in Logs & Errors** | Logging full HTTP headers or config dicts containing `Authorization: Bearer ...` | Strip or mask sensitive keys (`token`, `secret`, `password`, `authorization`) before logging or returning error payloads. |
| **`REV-05`** | **Strict Boundary Input Validation** | Accepting negative pagination (`?limit=-5`) or unbounded page sizes (`?limit=9999999`) | Enforce explicit bounds (`1 <= limit <= 100`) and return deterministic `400 / 422` errors. |

---

### ⚙️ Category B: Concurrency, State & I/O Resilience (`REV-06..11`)

| ID | Pattern Name | Anti-Pattern (`Rejected in Review ❌`) | Senior Production Pattern (`Approved ✅`) |
| :---: | :--- | :--- | :--- |
| **`REV-06`** | **Atomic File Writes (Zero Partial Corruption)** | `Path("state.json").write_text(data)` *(crash mid-write leaves a 0-byte corrupt file)* | Write to a temporary file in the same directory (`tempfile.NamedTemporaryFile`), `flush()` + `os.fsync()`, then `os.replace(tmp, target)`. |
| **`REV-07`** | **Explicit Network Timeouts Everywhere** | `requests.get(url)` or `http.Get(url)` with default infinite timeout | Always pass explicit connect + read timeouts (`timeout=(5, 15)` or `http.Client{Timeout: 10 * time.Second}`). |
| **`REV-08`** | **Idempotent Webhook & Event Deduplication** | Crediting a balance or firing an action twice when a webhook retries | Check and record a unique `event_id` / `reference_code` inside an atomic database transaction before executing side effects. |
| **`REV-09`** | **Bounded Retries with Exponential Backoff & Jitter** | `while True: retry()` or fixed `time.sleep(1)` on `HTTP 429 / 503` | Cap retries (`max_retries=3`), honor `Retry-After` headers, and use `base * (2 ** attempt) + random.uniform(0, 0.5)`. |
| **`REV-10`** | **Streaming Large Files (`O(1)` Memory)** | Reading an entire `.xdr.gz` or `.csv` archive into RAM with `.read()` | Stream via buffered readers (`io::BufReader` in Rust, `bufio.Scanner` in Go, generator chunks in Python). |
| **`REV-11`** | **Snapshot Integrity on Transient API Failure** | Overwriting cached state with `{}` when an upstream API returns a 502 error | Preserve the last known good state snapshot when a transient network or rate-limit failure occurs. |

---

### 🦀 Category C: Rust, Go & Type-Safe Systems Engineering (`REV-12..16`)

| ID | Pattern Name | Anti-Pattern (`Rejected in Review ❌`) | Senior Production Pattern (`Approved ✅`) |
| :---: | :--- | :--- | :--- |
| **`REV-12`** | **Zero `unwrap()` / `expect()` in Library Paths** | Using `.unwrap()` on user input, network bytes, or file I/O in Rust | Return typed `Result<T, DomainError>` with `?` propagation and actionable error messages. |
| **`REV-13`** | **Checked Integer Arithmetic** | `seq + 1` or `offset + frame_len` on untrusted 32/64-bit counters | Use `checked_add()` / `saturating_add()` to prevent integer overflow/wraparound panics. |
| **`REV-14`** | **Strict Binary Framing & End-of-Stream Checks** | Accepting trailing garbage bytes or truncated gzip/XDR streams silently | Verify exact frame byte lengths, RFC record-mark bits, and trailing checksums before marking a stream valid. |
| **`REV-15`** | **Backward-Compatible Public Signatures** | Breaking existing callers when adding a new CLI flag or struct field | Provide sensible defaults, builder methods, or optional config fields so existing callers compile unchanged. |
| **`REV-16`** | **HTTP `HEAD` vs `GET` Semantics** | Returning only `200 OK` on `HEAD` without `Content-Length`, `ETag`, or `Cache-Control` | Compute identical headers (`Content-Type`, `ETag`, `Cache-Control`, `Content-Length`) for both `GET` and `HEAD`, omitting only the body on `HEAD`. |

---

### 🧪 Category D: Deterministic Testing & Git Hygiene (`REV-17..19`)

| ID | Pattern Name | Anti-Pattern (`Rejected in Review ❌`) | Senior Production Pattern (`Approved ✅`) |
| :---: | :--- | :--- | :--- |
| **`REV-17`** | **Deterministic Offline Unit Tests** | Tests that call live external APIs or rely on `sleep(2)` wall-clock timing | Inject mock transports, fake clocks, or local ephemeral fixtures (`tempfile.TemporaryDirectory()`) so tests pass in `< 50ms` offline. |
| **`REV-18`** | **3-Case Boundary Coverage (`Happy`, `Corrupt`, `Edge`)** | Writing only 1 happy-path test | Always test: (1) Valid nominal input, (2) Corrupt/malformed input, and (3) Boundary conditions (`0`, `1`, `MAX`, gap in sequence). |
| **`REV-19`** | **Surgical Diff & Pre-Commit Formatter Parity** | Pushing unformatted code or touching 20 unrelated files | Run `cargo fmt --check`, `gofmt -s -l .`, `prettier --check`, or `ruff check` locally so the PR diff only touches the exact lines required. |

---

## 🤝 Contribute Your Own Lesson (Moderated Global Submissions)

Have you learned a valuable lesson from a real code review or engineering bug?
Submit a Pull Request adding `lessons/community/<your-username>-<topic>.json` following [`lessons/README.md`](../lessons/README.md)! Our **5-Gate Moderation Bot** will validate your lesson's schema, security, and quality automatically!
