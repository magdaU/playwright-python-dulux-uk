# 📊 Test Results

> A point-in-time record of the latest known execution result per test case and
> environment — the **narrative** counterpart to the [Test Summary Report](TEST_SUMMARY_REPORT.md)
> and the **live source of truth** for any given run is always the published Allure report
> (see [Getting Started — Reports](GETTING_STARTED.md#reports)), not this file. This
> document is refreshed after a significant regression pass, not on every push.

**Legend:** ✅ Pass · ⚠️ Pass with retry (logged + attached to Allure, see
[Lessons Learned #3](LESSONS_LEARNED.md#3-cross-engine-navigation-timing--the-same-interaction-behaves-differently-per-browser-engine)) · — Not yet executed in this configuration.

---

## Latest execution record

| TC ID | Scenario | Chromium | Firefox | WebKit | Last verified | Notes |
|---|---|---|---|---|---|---|
| TC-01 | Desktop customer adds a tester from the colour finder | ✅ | ✅ | ✅ | 2026-10-09 | Single run per engine after the performance changes (blocked third-party hosts, 15 s timeout): Firefox 59 s, WebKit 21 s. Whether the bounded shade-selection retry was used was not checked. Chromium last verified 2026-08-03 |
| TC-02 | Tablet customer adds a tester from the colour finder | ✅ | — | — | 2026-08-03 | Cross-browser matrix currently exercises `regression` generally; tablet-specific per-engine results not separately tracked yet |
| TC-03 | Mobile customer adds a tester from the colour finder | ✅ | — | — | 2026-08-03 | See TC-02 note |
| TC-04a | Tester quantity boundary values (1, 23, 0, 24) | ✅ | ✅ | ✅ | 2026-10-08 | Desktop, 4 examples, all engines. Cap of 23 is server-side (HTML declares `max=999`) |
| TC-06 | Shade with no tester option (negative path) | ✅ | ✅ | ✅ | 2026-10-08 | Desktop, "Cotton Breeze" under "Violet". Data-dependent: fails if the shade gains a tester |
| TC-04 | Basket increment/decrement/remove | ✅ | ✅ | ✅ | 2026-10-08 | Desktop; + / − / bin button |
| TC-05 | Add-to-basket failure is surfaced (stubbed HTTP 500) | ✅ | ✅ | ✅ | 2026-10-08 | Desktop; the error alert is short-lived, asserted as soon as it appears |
| TC-09 | Site search (known shade, unknown term, other letter case, part of a name) | ✅ | ✅ | ✅ | 2026-10-08 | Desktop; 2 examples; 2 more added 2026-10-09, Chromium only |
| TC-10 | Cookie banner blocks interaction until dismissed | ✅ | ✅ | ✅ | 2026-10-08 | Desktop; ids used because the banner text is localised |
| TC-07 | Desktop customer opens the Visualizer for a shade | ✅ | — | — | 2026-08-03 | |
| TC-08 | Mobile customer tries to open the Visualizer for a shade | ✅ | — | — | 2026-08-03 | Asserts the documented store-data message, not app success |
| TC-13 | Tester for shades from other colour families (Blue / Green) | ✅ | — | — | 2026-10-09 | Desktop; 2 examples, Chromium only so far |
| TC-14 | Basket shows tester price and order total | ✅ | — | — | 2026-10-09 | Desktop; seeded basket. Also fails when the expected price is changed (checked) |
| TC-15 | Basket survives a page reload | ✅ | — | — | 2026-10-09 | Desktop; seeded basket. Also fails when the expected quantity is changed (checked) |
| TC-20 | Mobile home page shows the menu, search and cart | ✅ | — | — | 2026-10-09 | Mobile viewport; Chromium only so far |
| TC-21 | Tablet home page shows the menu, search and cart | ✅ | — | — | 2026-10-09 | Tablet viewport; Chromium only so far |
| TC-19 | Cookie banner can be answered on a phone | ✅ | — | — | 2026-10-09 | Mobile viewport; Chromium only so far |
| TC-17 | Empty basket tells the customer so and offers a way back | ✅ | — | — | 2026-10-09 | Desktop; basket page only |
| TC-18 | Continue shopping leaves the basket for the product listing | ✅ | — | — | 2026-10-09 | Desktop; seeded basket. Also fails when the expected address is changed (checked) |
| TC-16 | A shade can be opened from the colour finder | ✅ | — | — | 2026-10-09 | Desktop; Chromium only so far |
| TC-12 | Home page shows the main navigation | ✅ | — | — | 2026-10-09 | Desktop; Chromium only so far. Home page load only |
| TC-11 | Shade page a11y scan (no new critical/serious violations) | ✅ | — | — | 2026-08-03 | Known violations allow-listed; scan itself run on Chromium as part of TC-01/TC-03 |

**Overall status as of the last full verification:** all 28 automated test cases (21 scenarios; two are
4-example outline) pass on
Chromium (the `smoke`-gating engine); Firefox and WebKit pass the `purchase` journey via
the documented, bounded retry rather than outright — see the risk register entry in
[Test Strategy §10](TEST_STRATEGY.md#10-risk-analysis--mitigations) ("Cross-engine
navigation timing").

---

## How this maps to CI

| Run mode | What it covers | Where to find current results |
|---|---|---|
| Push/PR smoke gate | TC-01, TC-07, TC-09 (2 examples), TC-10, TC-12, TC-14, TC-16, TC-17, TC-18, plus TC-20 (mobile) and TC-21 (tablet) (Chromium) | [`e2e-tests.yml`](../.github/workflows/e2e-tests.yml) run history + Allure report on GitHub Pages |
| Cross-browser regression | All `regression`-marked scenarios × Chromium/Firefox/WebKit | [`cross-browser-regression.yml`](../.github/workflows/cross-browser-regression.yml) run history |
| Nightly regression | All `regression`-marked scenarios, Chromium, daily | [`nightly-regression.yml`](../.github/workflows/nightly-regression.yml) run history (uploaded as a build artifact) |

## Historical incidents affecting results

Three past failures materially changed what "pass" means for this suite — both fully
root-caused rather than papered over:

- **2026-07-09** — `purchase` scenarios failed because "Gentle Lavender" had been removed
  from the "Violet" family on production. Test data refreshed to "Violet Morning".
- **2026-10-08** — nightly `regression` failed: "Violet Morning" still existed but no longer
  offered "Buy a Tester in this colour". Test data changed to "Romantic Reverie", verified to
  offer a tester.
- **2026-08-03** — `purchase` scenarios failed on the basket-quantity assertion after a
  production markup redesign broke locator uniqueness. Fixed by narrowing the locator to
  role `spinbutton`.

Full incident write-ups: [Lessons Learned](LESSONS_LEARNED.md).

## See also

- [Test Cases](TEST_CASES.md) — what each TC ID actually verifies.
- [Test Summary Report](TEST_SUMMARY_REPORT.md) — cycle-level narrative and recommendation.
- [Test Plan](TEST_PLAN.md) — schedule and environments these results were produced under.
