# 📓 Lessons Learned

> Concrete incidents this suite has hit while running against a real, live production
> site — what happened, the root cause, the fix, and the takeaway. Full risk-register
> context lives in [Test Strategy §10](TEST_STRATEGY.md#10-risk-analysis--mitigations);
> this document is the narrative, incident-by-incident version.

---

## 1. Product catalogue drift — a pinned shade disappeared from its colour family

**What happened:** the `purchase` scenarios' test data used shade "Gentle Lavender" from
the "Violet" family. Mid-project, the shade was found to have been quietly removed from
that family on production, breaking both this suite and its Java sibling identically.

**Root cause:** the SUT is the real, public Dulux catalogue — not a fixture we control.
Retailers add/remove/re-group products without notice.

**Fix:** refreshed the test data to "Violet Morning", confirmed present in the catalogue.

**Considered and rejected:** a "self-healing" alternative — pick whatever shade the
colour-finder lists first, instead of a fixed name. Investigated and found that not every
shade has a tester available for direct purchase; the first shade the catalogue actually
returned ("Cotton Breeze") only exposed a "Find Products in this colour" flow, no "Buy a
Tester" button. A real self-healing version would need to loop candidates until one with a
tester is found — real added complexity for a risk that had, at that point, only
materialised once (Medium likelihood, not High). **Decision:** keep the pinned, verified
shade name and re-evaluate if it drifts again, rather than build speculative resilience
for a problem that hasn't recurred.

**Lesson:** a pinned, human-verified test value plus fast re-verification beats a
"self-healing" mechanism that trades a rare, cheap-to-fix problem for permanent extra
complexity and its own new failure modes.

---

## 2. Basket UI markup drift — a redesign broke a locator's *uniqueness*, not its match

**What happened:** while verifying cross-browser support, the basket's quantity control
had been redesigned into a `group` wrapping decrease/input/increase controls — all three
now exposed an accessible name containing "Quantity". `get_by_label("Quantity")` in
`cart_page.py` went from matching exactly 1 element to matching 4, failing Playwright's
strict-mode uniqueness check.

**Root cause:** the original locator matched on a substring of the accessible name, which
was unique only by accident — nothing about it *required* uniqueness once the markup grew
more elements with a similar label.

**Fix:** narrowed to `get_by_role("spinbutton", name="Quantity input")`, which targets the
input specifically by role rather than any element merely labelled "Quantity".

**Lesson:** a locator can pass today for the wrong reason. Prefer the most *specific*
role-based match available, not just the first one that happens to resolve uniquely — the
failure mode when it breaks (strict-mode violation) is at least loud and immediate rather
than silently clicking the wrong element.

---

## 3. Cross-engine navigation timing — the same interaction behaves differently per browser engine

**What happened:** running the `purchase` journey against production with `--browser
firefox`/`webkit` showed both engines unreliably picking up the "Violet" colour-family
filter before the next step queried for a shade button — a real `TimeoutError`, not a
selector problem. Chromium never exhibited this.

**Root cause:** a genuine per-engine difference in how the client-side filter interaction
settles, on a page we don't own and can't instrument further.

**Fix:** a bounded (3-attempt), *explicit* retry in `support/retry.py`, applied only to
this one identified interaction — not a blanket retry wrapper around every step. Every
attempt (pass or fail) is logged and attached to the Allure report, so a green run is
never silently indistinguishable from one that needed a retry to get there.

**Also mitigated by:** keeping cross-browser coverage on a separate, on-demand
[`cross-browser-regression.yml`](../.github/workflows/cross-browser-regression.yml)
workflow rather than gating every push on it — a real per-engine timing difference
shouldn't make the fast push/PR gate flaky for reasons unrelated to the code under test.

**Lesson:** when flakiness is investigated and found to be a genuine environment/engine
difference (not a bad wait), the right fix is a narrow, visible, bounded retry on exactly
that interaction — never a broad retry-everything policy that would hide the difference
between "flaky" and "actually broken."

---

## 4. Pre-existing accessibility violations on a site we don't own

**What happened:** an `axe-core` scan of the shade page found a real `critical`
violation (`image-alt`) and a `serious` one (`color-contrast`) on desktop, plus a second
`critical` (`label`) on mobile — genuine, pre-existing production defects.

**Root cause:** we're testing a third-party site; we can't fix its accessibility issues,
only detect regressions in them.

**Fix:** the known violation IDs are allow-listed by ID in `support/accessibility.py`. The
suite still fails the build on any *new* critical/serious violation, so it keeps real
signal without permanently reddening the build for defects outside our control.

**Lesson:** "gate on everything" (permanently red, ignored by the team) and "gate on
nothing" (no signal at all) are both worse than a documented, ID-based allow-list — a
pragmatic middle ground that keeps the gate meaningful.

---

## 5. "The build succeeded" ≠ "the container runs"

**What happened:** `docker compose build` completed successfully — Python deps, Chromium +
OS deps, non-root user setup all passed, producing a working-looking image. Weeks later,
`docker compose up` was found to fail 100% of the time: every step-definition module's
`from support.context import Context` raised `ModuleNotFoundError` at collection time.

**Root cause:** the Dockerfile's `COPY` list copied `pages`, `features` and `tests`, but
never `support/`. `COPY` doesn't fail when a source directory is simply missing from the
list — there's no error at build time, only a broken runtime.

**Fix:** added `COPY support ./support`; re-verified end-to-end with `docker run` against
production (the smoke suite actually passes inside the container, not just "the image
exists").

**Lesson:** a successful build is a claim about the build step, not about the running
container — verifying "it builds" and verifying "it runs" are two different checks, and
only the first one had actually been exercised before this was caught.

---

## 6. Visual regression — deferred, not skipped

**What happened:** visual/pixel-diff regression testing was considered for key pages.

**Why it was deferred:** in the same working session, the basket page markup was found
to have been redesigned (incident #2 above) *and* the shade catalogue had already drifted
once before (incident #1) — two concrete, recent signs this production site's layout is
still actively changing. Snapshotting now would bake in a baseline that goes stale at the
next incidental UI tweak, producing pixel-diff noise on changes that aren't real
regressions — directly against the guiding principle that a red build must mean a real
regression.

**Decision:** re-evaluate once a period passes without an unannounced layout change,
rather than adding a check now that would be noisy by construction.

**Lesson:** a technique can be right in general and still wrong *right now* — timing a
mitigation against the actual, observed rate of change in the thing it protects matters as
much as the mitigation itself.

---

## 7. A pinned dependency can hide a ticking compatibility problem

**What happened:** every test run emits a `PytestRemovedIn10Warning` from
`pytest_bdd/compat.py` — `pytest-bdd` 8.1.0 relies on internal pytest fixture-scoping APIs
(`_register_fixture` called with `nodeid`/`baseid` instead of `node`) that are slated for
removal in pytest 10.

**Root cause:** `pytest-bdd` depends on pytest internals, not just its public API surface.

**Current state:** harmless today because `pytest` is pinned to `9.1.1` — but bumping
pytest to `10.x` without a `pytest-bdd` fix first would break test collection outright.

**Lesson:** a passing, warning-only build can still be carrying a scheduled breakage.
Documenting *why* a warning is currently safe to ignore — and what would make it stop being
safe — is worth doing at the moment it's noticed, not left for whoever runs the next
dependency bump to rediscover from scratch.

---

## See also

- [Test Strategy §10 — Risk analysis & mitigations](TEST_STRATEGY.md#10-risk-analysis--mitigations) — the same incidents as a likelihood/impact register.
- [Test Strategy §13 — Maintenance & roadmap](TEST_STRATEGY.md#13-maintenance--roadmap) — where each fix sits in the project's timeline.
- [Getting Started](GETTING_STARTED.md) — install, run, and day-to-day developer/tester workflow.
