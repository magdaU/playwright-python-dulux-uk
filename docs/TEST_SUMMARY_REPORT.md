# 📝 Test Summary Report

> A cycle-level, stakeholder-facing summary: what was tested, the outcome, defects found
> and their resolution, residual risk, and a recommendation. Where [Test Results](TEST_RESULTS.md)
> is the detailed per-case record, this is the narrative a team lead or hiring reviewer
> would actually read.

| | |
|---|---|
| **Reporting period** | Project inception → 2026-09-04 (ongoing; suite runs continuously, not as a single campaign) |
| **Product under test** | Dulux UK e-commerce website (`https://www.dulux.co.uk`) |
| **Report author** | QA / SDET |
| **Related documents** | [Test Plan](TEST_PLAN.md) · [Test Results](TEST_RESULTS.md) · [Lessons Learned](LESSONS_LEARNED.md) |

---

## 1. Summary

The suite automates the two highest-value Dulux UK customer journeys — **tester
purchase** and **Visualizer launch** — across desktop, tablet and mobile viewports, with
an accessibility scan folded into the purchase journey. All 5 scenarios currently pass
against live production on the primary engine (Chromium); the `purchase` journey also
passes on Firefox and WebKit via a documented, bounded retry for one known cross-engine
timing difference.

## 2. Scope executed

| Journey | Viewports | Status |
|---|---|---|
| Tester purchase | Desktop, tablet, mobile | ✅ Passing |
| Visualizer | Desktop, mobile | ✅ Passing |
| Accessibility (shade page) | Desktop, mobile | ✅ Passing (against an allow-listed baseline) |

Out of scope for this cycle (and for the suite generally): checkout/payment, account/login,
API/contract testing, performance/load, full visual regression — see
[Test Strategy §3](TEST_STRATEGY.md#3-scope) for the rationale and
[Test Strategy §14](TEST_STRATEGY.md#14-coverage-gaps--improvement-opportunities) for what
closing each gap would take.

## 3. Results at a glance

- **5 / 5** automated scenarios passing on the primary engine (Chromium).
- **0** open defects — every issue found during development was root-caused and fixed
  (see §4).
- **1** accepted, documented residual risk pattern: genuine per-engine timing differences
  on Firefox/WebKit, mitigated by a bounded, visibly-reported retry rather than hidden.

Full per-case, per-browser breakdown: [Test Results](TEST_RESULTS.md).

## 4. Defects found during testing

All defects below were found by this suite while testing against real production — none
were seeded or simulated. Each is fully written up in [Lessons Learned](LESSONS_LEARNED.md).

| # | Defect | Severity | Status |
|---|---|---|---|
| 1 | Product catalogue drift — pinned test shade removed from its colour family | Medium | ✅ Fixed (test data refreshed) |
| 2 | Basket UI redesign broke a locator's uniqueness (quantity control) | Medium | ✅ Fixed (locator narrowed to role) |
| 3 | Cross-engine navigation timing difference (Firefox/WebKit) | Medium | ✅ Mitigated (bounded, reported retry) |
| 4 | Pre-existing a11y violations on the shade page (not owned by this team) | Medium | ✅ Handled (allow-listed by ID, new violations still gate) |
| 5 | Docker image built successfully but the container failed 100% of the time (`support/` missing from `COPY`) | High | ✅ Fixed |

None of these are open defects against the current suite — all are resolved or
consciously mitigated, and the fix/decision for each is documented rather than silently
applied.

## 5. Test environment

Executed against live production (`dulux.co.uk`) from GitHub Actions `ubuntu-latest`
(headless) for CI runs, and locally (headed/headless, or via Docker) for authoring —
see [Test Plan §9](TEST_PLAN.md#9-environmental-needs). No staging/sandbox environment is
available for this third-party site.

## 6. Residual risk

The single largest structural risk remains **testing against live production** — content,
layout and third-party behaviour can change at any time, independent of any code change
in this repository. This is a deliberate trade-off (realistic coverage, at the cost of
occasional environment-driven failures) rather than an oversight — see
[Test Strategy §10](TEST_STRATEGY.md#10-risk-analysis--mitigations) for the full register
and how each risk is mitigated today.

## 7. Recommendation

**Go** — the two in-scope revenue/engagement journeys are verified working across all
targeted viewports, on all three browser engines, with accessibility regressions gated and
known production issues explicitly and transparently allow-listed. No open defects.
Recommended next investments, in priority order, are listed in
[Test Strategy §14](TEST_STRATEGY.md#14-coverage-gaps--improvement-opportunities).

## 8. Sign-off

Single-contributor project — this report is self-issued by QA/SDET and reviewed via the
normal PR process before being merged into `main`.
