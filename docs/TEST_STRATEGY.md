# 🧭 Test Strategy — Dulux UK E2E Automation (Python)

> Living document. It describes **what** we test, **why**, and **how** the automation
> framework in this repository is designed to deliver fast, trustworthy feedback on the
> [Dulux UK](https://www.dulux.co.uk) customer journeys. Python port of
> [playwright-java-dulux-uk](https://github.com/magdaU/playwright-java-dulux-uk) — same
> journeys, same strategy, different stack.

| | |
|---|---|
| **Product under test** | Dulux UK e-commerce website (`https://www.dulux.co.uk`) |
| **Test type** | UI end-to-end (black-box, browser-driven) |
| **Framework** | Playwright for Python · pytest-bdd · pytest · Allure |
| **Pipeline** | GitHub Actions → smoke suite on every push/PR, report published to GitHub Pages |
| **Owner** | QA / SDET |
| **Status** | Skeleton — feature files and step signatures are ported, step bodies and page object methods are `NotImplementedError` stubs. Collection, marker filtering and the desktop/mobile Playwright fixtures are verified end-to-end against a live browser and dulux.co.uk; business step implementation is the next milestone (see §13). |

---

## 1. Purpose & objectives

The goal of this automation is **not** to test everything the Dulux site does — it is to
continuously prove that the **highest-value customer journeys still work** across the
viewports our customers actually use.

Quality objectives, in priority order:

1. **Protect revenue paths** — a customer must always be able to find a colour and add a
   tester to the basket. This is the critical, money-making flow.
2. **Protect cross-device parity** — the same journey must work on desktop and mobile,
   which use *different* navigation (top nav vs. hamburger menu).
3. **Fast, actionable feedback** — every push runs the smoke suite headless in CI in
   minutes, with a published Allure report.
4. **Trustworthy results** — a red build means a real regression, not a flaky test. Test
   stability is treated as a first-class feature, not an afterthought.

---

## 2. System under test (SUT)

The SUT is the **live, public production** Dulux UK website. This is deliberate (it gives
realistic coverage) but it is also the single biggest source of risk (see §10).

Characteristics that shape the test design:

- JavaScript-heavy SPA-style storefront with client-side navigation.
- A cookie consent banner that blocks interaction until dismissed.
- "Find a colour" flow that triggers a **full page navigation** (not a dropdown).
- A Visualizer link that opens in a **new browser tab**.
- Responsive layouts: desktop exposes a top navigation bar; mobile collapses it behind a
  hamburger menu.
- Third-party dependencies (analytics, the Adjust-powered Visualizer) that can return
  environment-specific messages.

---

## 3. Scope

### ✅ In scope

| Area | Covered journeys |
|---|---|
| **Tester purchase** | Browse to a shade via the colour finder and add a tester to the basket (desktop + mobile) |
| **Visualizer experience** | Open the Visualizer from a selected shade page (desktop opens a new tab; mobile surfaces the store-data message) |
| **Cross-viewport** | Every journey runs at desktop `1920×1080` and mobile `375×667` |
| **Cookie consent** | Implicitly exercised — every journey rejects cookies before proceeding |

### ❌ Out of scope (for this suite)

- Checkout, payment and order fulfilment (no transactions against production).
- Account creation, login and profile management.
- API / service-level, contract, unit and component testing (the app is third-party; we
  own no production code to unit-test, and Dulux exposes no API to test against).
- Performance, load and stress testing.
- Accessibility (a11y) and full cross-browser matrix — **candidates for the roadmap (§13)**.
- Visual regression / pixel comparison.

> **Note on the test pyramid.** This repository is intentionally an **E2E layer only**,
> because we do not own the application code. We compensate for the known cost of E2E
> (slower, more brittle) by keeping the suite small, journey-focused, and tag-sliced so the
> critical `smoke` set stays fast.

---

## 4. Test approach

### 4.1 Levels & style

- **Behaviour-Driven (BDD)** — journeys are described in business-readable Gherkin
  (`*.feature`) so intent is reviewable by non-engineers. `pytest-bdd` binds each
  scenario to a test function via `scenarios()`; Gherkin tags become pytest markers
  automatically, so tagging and filtering need no separate configuration layer.
- **Single entry point** — unlike the Java version (which keeps a parallel plain-JUnit
  suite alongside Cucumber), this project uses `pytest-bdd` as the only test entry point.
  There is no second, hand-rolled journey implementation to keep in sync.

### 4.2 Design principles

| Principle | How it's applied |
|---|---|
| **Page Object Model** | Each page (`HomePage`, `ColorSelectionPage`, `CartPage`) and reusable component (`NavigationComponent`, `AlertComponent`) extends a shared `BasePage`. UI locators live in one place. |
| **No assertions in page objects** | Pages only *act* and *expose* locators. All assertions live in the step layer (plain `assert`, rewritten by pytest for rich failure output — no fluent-assertion library needed). |
| **Fixtures instead of a DI container** | The Java project injects a shared `CucumberContext` via PicoContainer. Here, `conftest.py` fixtures (`desktop_page`, `mobile_page`, and the `browser`/`context` fixtures `pytest-playwright` provides for free) fill the same role idiomatically. |
| **Role-based locators** | Locators prefer `get_by_role` / `get_by_label` / `get_by_text` over brittle CSS/XPath, matching how a user perceives the page and surviving DOM churn. |
| **Web-first waits** | Playwright's auto-waiting assertions replace manual sleeps; explicit `wait_for_load_state()` is used only where a real navigation occurs. |

### 4.3 Test design techniques

- **Scenario / user-journey based** — each test mirrors a real customer task end to end.
- **Equivalence partitioning** — one representative shade (`Gentle Lavender` / `Violet`)
  stands in for the colour-finder space; the *flow*, not the data permutation, is the risk.
- **State verification** — basket starts empty → exactly 1 item with the right product and
  shade after adding (guards against silent over/under-counting).
- **Cross-configuration testing** — desktop vs. mobile as distinct navigation paths and
  distinct pytest fixtures (`desktop_page` / `mobile_page`).

---

## 5. Test data strategy

- **Data is inline and self-describing** in the Gherkin (shade name, colour family,
  expected product label) — no external fixtures to drift out of sync.
- **No persistent data is created** on production: the basket flow stops *before* checkout,
  and each scenario runs in a fresh, isolated Playwright `BrowserContext` (no shared
  cookies/storage) via the `desktop_page` / `mobile_page` fixtures, so runs never
  contaminate one another.
- **Self-cleaning** — because no order is placed and contexts are disposed after every
  scenario (`conftest.py` closes the context on fixture teardown), there is no
  teardown/data-reset burden.

---

## 6. Environments

| Environment | Where | Purpose |
|---|---|---|
| **Local (headed)** | Developer machine, `pytest --headed` | Authoring and debugging — watch the journey run |
| **Local (headless)** | `pytest` (headless is the `pytest-playwright` default) | Fast local verification before pushing |
| **Docker** | `docker compose up --build` | Reproducible run matching CI (Python 3.12 + Chromium, `shm_size: 1gb`) |
| **CI** | GitHub Actions `ubuntu-latest`, headless | Gate on every push/PR; publishes the Allure report |

Headless/headed is resolved by `pytest-playwright`'s built-in `--headed` CLI flag — no
hand-written config class is needed (the Java project's `PlaywrightConfig` has no
equivalent here).

---

## 7. Tooling

| Concern | Tool |
|---|---|
| Browser automation | Playwright for Python (Chromium) |
| Test runner | pytest |
| BDD | pytest-bdd |
| Assertions | Playwright web-first assertions + plain `assert` |
| Fixtures / DI | pytest fixtures (`conftest.py`) |
| Reporting | Allure (`allure-pytest-bdd`) |
| CI/CD | GitHub Actions, GitHub Pages |
| Containerisation | Docker / Docker Compose |
| Dependency management | pip + `requirements.txt` |

---

## 8. Test selection & tagging strategy

Gherkin tags are the contract between "what changed" and "what we run" — `pytest-bdd`
converts them into pytest markers automatically, so `@smoke` in a `.feature` file becomes
`-m smoke` on the command line, no extra mapping step required.

| Marker | Meaning | When it runs |
|---|---|---|
| `smoke` | Minimal critical-path set, fast | **Every push & PR** (CI default) |
| `regression` | Full journey coverage | On demand / scheduled / pre-release |
| `desktop` | Desktop-viewport variant | Filtered as needed |
| `mobile` | Mobile-viewport variant | Filtered as needed |
| `purchase`, `visualizer` | Feature grouping | Targeted debugging of one journey |

Selection is driven by `pytest -m "..."` (CI defaults to `smoke`, overridable via the
`workflow_dispatch` input or the `PYTEST_MARKERS` env var in Docker).

---

## 9. CI/CD & reporting

**Pipeline** ([`.github/workflows/e2e-tests.yml`](../.github/workflows/e2e-tests.yml)):
checkout → Python 3.12 → install dependencies → install Chromium → run smoke suite
headless → generate Allure report → upload artifacts → publish to GitHub Pages (on `main`).

**Reporting layers:**

- **Allure** (`allure-pytest-bdd`) — the primary dashboard, with Gherkin steps rendered
  per scenario. History is carried across builds via `gh-pages` for the **Trend** widget.
- No separate HTML/XML report is generated today (the Java project also produces a
  standalone Cucumber HTML report) — Allure is the single reporting layer for now.

**Key metrics tracked:** pass/fail rate and trend, per-step duration, and flaky-test
signals (a test that fails then passes on re-run without a code change).

---

## 10. Risk analysis & mitigations

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| **Testing against live production** — content/layout/availability can change at any time | High | High | Role/label/text-based locators that tolerate DOM change; small focused suite; treat unexpected failures as *signal* and triage fast |
| **Cookie banner / consent variations** block interaction | Medium | High | Cookies are explicitly rejected at the start of every journey |
| **Flakiness** from network, animations, third-party scripts | Medium | High | Playwright auto-waiting, isolated `BrowserContext` per scenario, `shm_size: 1gb` in Docker to prevent Chromium crashes |
| **Third-party Visualizer/Adjust** returns environment-specific messages | Medium | Medium | Mobile scenario asserts the known store-data message rather than assuming success; behaviour is documented, not hidden |
| **New-tab handling** for the Visualizer | Low | Medium | Playwright's `expect_page()` context manager captures the popup deterministically on desktop |
| **Single browser (Chromium) only** | Medium | Low | Accepted for now; cross-browser is on the roadmap (§13) |
| **Step bodies not yet implemented** | High (today) | High (today) | Tracked openly in this document's status line rather than hidden; collection/tagging/fixtures are verified independently so implementation is the only remaining gap |

---

## 11. Entry & exit criteria

**Entry (a build is allowed to run the suite):**

- Dependencies install (`pip install -r requirements.txt`) and the Chromium browser
  installs successfully (`playwright install --with-deps chromium`).
- `pytest --collect-only` succeeds (proves feature parsing, step binding and marker
  mapping are intact before spending time on a real browser run).

**Exit (a build/release is considered green):**

- 100% of `smoke`-marked scenarios pass on both viewports.
- Any failure is triaged to a root cause (real regression vs. environment/flake) before the
  result is trusted.

---

## 12. Roles & responsibilities

| Role | Responsibility |
|---|---|
| **SDET / QA** | Own the framework, author scenarios, triage failures, keep the suite stable |
| **Reviewers** | Read Gherkin to confirm scenarios describe the *right* behaviour |
| **CI** | Run the smoke gate on every push/PR and publish the report |

---

## 13. Maintenance & roadmap

Planned work, roughly in priority order:

- [ ] **Implement step bodies & page objects** — port the working locators/logic from
  `playwright-java-dulux-uk`; today's stubs raise `NotImplementedError` by design.
- [ ] **Verify the Docker build** — `Dockerfile`/`docker-compose.yml` exist and
  `docker compose config` validates, but a full `docker build` has not yet been run
  successfully in this environment.
- [ ] **Cross-browser** — add Firefox and WebKit to widen real coverage.
- [ ] **Accessibility checks** — integrate an a11y scan into the critical journeys.
- [ ] **Tablet viewport** — a third breakpoint between mobile and desktop.
- [ ] **Retry policy for known-flaky steps** — bounded, explicit, and reported (never silent).
- [ ] **Scheduled regression run** — nightly `regression`-marked run against production to
  catch drift.
- [ ] **Visual regression** — snapshot key pages once layouts stabilise (see the Java
  project's `image-comparison`-based approach for a reusable pattern).

---

> **Guiding principle:** keep the suite **small, fast, and trustworthy**. A test that is
> flaky or slow is worse than no test, because it erodes confidence in the green build.
