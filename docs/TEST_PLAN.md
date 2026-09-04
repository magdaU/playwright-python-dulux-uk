# 📋 Test Plan

> Where the [Test Strategy](TEST_STRATEGY.md) explains *what we test and why* as a living,
> ongoing document, this Test Plan is the execution-facing artifact for a given test
> cycle — scope, schedule, environment, roles, entry/exit criteria and sign-off. It's
> written generally enough to apply to any run of this suite (a push/PR gate, an on-demand
> cross-browser pass, or the nightly regression), noting where each differs.

| | |
|---|---|
| **Plan owner** | QA / SDET (single-contributor project) |
| **Product under test** | Dulux UK e-commerce website (`https://www.dulux.co.uk`) |
| **Test basis** | No internal requirements/specs available — see [Testing Without Requirements](TESTING_WITHOUT_REQUIREMENTS.md) for how scope was derived instead |
| **Related documents** | [Test Strategy](TEST_STRATEGY.md) · [Test Cases](TEST_CASES.md) · [Features Guide](FEATURES_GUIDE.md) |

---

## 1. Objectives

Prove, on a recurring and automated basis, that the two highest-value customer journeys —
**buying a colour tester** and **launching the Visualizer** — keep working across the
viewports real customers use, with fast enough feedback that a red build is trusted and
acted on.

## 2. Test items (in scope for this plan)

- Tester purchase journey — desktop, tablet, mobile (TC-01 – TC-03).
- Visualizer journey — desktop, mobile (TC-07, TC-08).
- Accessibility scan on the shade page, both viewports (TC-11).

See [Test Cases](TEST_CASES.md) for full specifications and [Test Strategy §3](TEST_STRATEGY.md#3-scope)
for the scope rationale, including what's explicitly excluded (checkout, login, API/contract,
performance, full visual regression).

## 3. Features not tested

Checkout/payment, account/login, backend API contracts, performance/load, and pixel-level
visual regression — see [Test Strategy §3](TEST_STRATEGY.md#3-scope) for why each is out,
and [Test Strategy §14](TEST_STRATEGY.md#14-coverage-gaps--improvement-opportunities) for
what it would take to bring each in scope.

## 4. Approach

- **BDD, black-box, browser-driven** — Gherkin scenarios in `features/`, executed via
  `pytest-bdd` against the real production site (no mocks, no staging environment
  available). See [Test Strategy §4](TEST_STRATEGY.md#4-test-approach).
- **Tag-sliced execution** — `smoke` (fast, desktop-only, gates every push/PR),
  `regression` (full viewport matrix, on-demand and nightly). See [Test Strategy §8](TEST_STRATEGY.md#8-test-selection--tagging-strategy).
- **Three run modes**, each with a different cadence/purpose:

  | Mode | Trigger | Marker | Browser(s) |
  |---|---|---|---|
  | Push/PR gate | Every push to `main`/`feature/**`/`fix/**`, every PR | `smoke` | Chromium |
  | Cross-browser regression | Manual (`workflow_dispatch`) | `regression` (default) | Chromium, Firefox, WebKit |
  | Nightly regression | Scheduled, `02:00 UTC` daily | `regression` | Chromium |

## 5. Item pass/fail criteria

A test case **passes** when its documented "Expected result" holds and no assertion
raises. A test case **fails** when an assertion fails *or* when Playwright itself raises
(e.g. a locator times out) — both are captured in the Allure report with full step detail.

## 6. Suspension & resumption

- **Suspend a run** if `pytest --collect-only` fails (a structural problem — broken
  feature/step-def wiring — not a real product regression; see entry criteria below).
- **Do not suspend** on a single scenario failure — triage it individually; a red build
  from one broken journey shouldn't hide signal from the others.
- **Resume** once the collection error is fixed and `pytest --collect-only` passes again.

## 7. Entry & exit criteria

Reused from [Test Strategy §11](TEST_STRATEGY.md#11-entry--exit-criteria):

**Entry:** dependencies and Chromium install cleanly; `pytest --collect-only` succeeds.

**Exit:** 100% of `smoke`-marked scenarios pass on both viewports; any failure is
root-caused (real regression vs. environment/flake) before the result is trusted — never
silently re-run until green.

## 8. Test deliverables

- Gherkin feature files ([`features/`](../features/)) — the readable spec of what's tested.
- Allure report — published to GitHub Pages on every `main` merge; local via
  `allure serve allure-results` ([Getting Started](GETTING_STARTED.md#reports)).
- [Test Results](TEST_RESULTS.md) — latest known execution record per test case/environment.
- [Test Summary Report](TEST_SUMMARY_REPORT.md) — narrative outcome per cycle, defects
  found, and a go/no-go recommendation.

## 9. Environmental needs

| Environment | Purpose |
|---|---|
| Local, headed (`pytest --headed`) | Authoring & debugging |
| Local, headless (`pytest`) | Fast pre-push verification |
| Docker (`docker compose up --build`) | Reproducible run matching CI |
| CI — GitHub Actions `ubuntu-latest`, headless | The gating environment |

No staging/sandbox environment exists — every run targets live production, which is
itself the largest single risk to this plan (see [Test Strategy §10](TEST_STRATEGY.md#10-risk-analysis--mitigations)).
Internet access to `dulux.co.uk` is a hard prerequisite everywhere.

## 10. Roles & responsibilities

Reused from [Test Strategy §12](TEST_STRATEGY.md#12-roles--responsibilities) — on this
solo project, QA/SDET owns authoring, execution, triage and maintenance end to end; CI
owns unattended execution and report publishing; a PR reviewer's role is to read the
Gherkin and confirm it describes the *right* behaviour.

## 11. Schedule

There is no fixed test-cycle calendar — this is a continuously-run suite, not a
point-in-time test campaign:

- **Continuous:** `smoke` on every push/PR (minutes).
- **Daily:** nightly `regression`, `02:00 UTC`.
- **On demand:** cross-browser `regression`, triggered manually before anything
  cross-engine-sensitive ships, or periodically to catch drift.

## 12. Risks & contingencies

Full risk register: [Test Strategy §10](TEST_STRATEGY.md#10-risk-analysis--mitigations).
Key ones affecting this plan specifically:

- **No staging environment** — every run is against production; contingency is a small,
  role/label-based, easily-triaged suite rather than broad coverage (§1 of the Test
  Strategy).
- **Production drift** (catalogue, markup, third-party behaviour) can fail a run for
  reasons outside our control — contingency is fast triage and, where a fix is warranted,
  a documented incident (see [Lessons Learned](LESSONS_LEARNED.md)).

## 13. Approval

Single-contributor project — plan changes are made directly by QA/SDET, reviewed via
normal PR review before merging into `main`.
