# Getting Started

## Overview

Python port of [playwright-java-dulux-uk](https://github.com/magdaU/playwright-java-dulux-uk) — the **same** real Dulux UK customer journeys (buy a colour tester, launch the Visualizer app), the **same** Page Object Model + BDD architecture, a different stack (`pytest-bdd` + plain pytest fixtures instead of Cucumber + PicoContainer DI).

> **Status:** implemented and verified against production — all 5 scenarios pass (desktop + tablet + mobile `purchase`, desktop + mobile `visualizer`).

📚 **Docs:** [Features Guide](FEATURES_GUIDE.md) (functional walkthrough of the site areas under test) · [Test Strategy](TEST_STRATEGY.md) (what we test, why, scope, risk analysis, roadmap) · [Test Plan](TEST_PLAN.md) · [Test Cases](TEST_CASES.md) · [Test Results](TEST_RESULTS.md) · [Test Summary Report](TEST_SUMMARY_REPORT.md) · [Architecture](ARCHITECTURE.md) (tech stack, design rationale, project structure, a full sample scenario walkthrough) · [Lessons Learned](LESSONS_LEARNED.md) · [Testing Without Requirements](TESTING_WITHOUT_REQUIREMENTS.md).

## What This Project Demonstrates

This isn't a toy TODO-app suite — it's built against a real, live production e-commerce
site, which surfaces the same problems a professional QA/SDET role deals with day to day:

- **Risk-based test strategy, not just test scripts** — [Test Strategy](TEST_STRATEGY.md)
  defines scope with explicit trade-offs (what's deliberately *out*, and why), a
  prioritised risk register, and entry/exit criteria — the kind of document a team lead
  reviews before trusting a suite's "green".
- **Real bugs found and triaged, not simulated ones** — this suite has caught genuine
  production issues while it was being built: a colour shade quietly removed from its
  family (catalogue drift), a basket control redesign that broke a locator's uniqueness,
  and a genuine cross-browser navigation-timing difference. Each is root-caused and
  documented in [Test Strategy §10](TEST_STRATEGY.md#10-risk-analysis--mitigations)
  rather than papered over with a blanket retry.
- **Judgement calls, documented** — e.g. "self-healing" shade selection and visual
  regression were both seriously considered and **deliberately rejected** for now, with the
  reasoning kept in the roadmap ([§13](TEST_STRATEGY.md#13-maintenance--roadmap))
  instead of silently dropped.
- **Engineering discipline in the framework itself** — Page Object Model with no
  assertions in page objects, role-based locators over brittle CSS/XPath, web-first waits
  instead of sleeps, and a `ruff` lint/format gate enforced in CI.
- **Pragmatic accessibility testing** — `axe-core` scans that fail the build on *new*
  critical/serious violations while allow-listing known, pre-existing production issues
  the team doesn't own — a real-world compromise between "gate on everything" and "gate on
  nothing".
- **CI/CD pipeline design, not just a green checkmark** — three purpose-built GitHub
  Actions workflows (push/PR smoke gate, on-demand cross-browser matrix, scheduled nightly
  regression) kept deliberately separate so flaky cross-engine differences never block a
  merge, with Allure history/trend published to GitHub Pages.
- **Debugging past "it builds"** — the Docker image build succeeded while the container
  itself failed 100% of the time (`support/` was missing from the `COPY` list); the fix and
  the lesson ("build succeeded" ≠ "container runs") are documented in
  [Test Strategy §13](TEST_STRATEGY.md#13-maintenance--roadmap).
- **Stack-agnostic QA design** — the same architecture and strategy exist in
  [a Java/Cucumber sibling project](https://github.com/magdaU/playwright-java-dulux-uk),
  showing this is a transferable way of thinking about test design, not a one-language trick.

## Key Features

- 🧱 **Page Object Model + Component Objects**, no assertions in page objects — all `expect()`/`assert` calls live in the step layer.
- 🥒 **BDD with pytest-bdd** — Gherkin `@tag`s become pytest markers automatically, filterable with `-m "smoke"` etc.
- 📱 **Cross-viewport coverage** — `purchase` at desktop/tablet/mobile, `visualizer` at desktop/mobile, via dedicated viewport fixtures.
- ♿ **Accessibility scanning** — `axe-core` on the shade page; known pre-existing production violations are allow-listed by ID so the suite still catches *new* ones.
- 🔁 **Bounded, reported retries** for the one interaction identified as genuinely flaky across browser engines — every attempt logged and attached to the Allure report.
- 🌐 **Cross-browser & nightly regression** — Chromium/Firefox/WebKit on demand, full regression suite scheduled daily against production.
- 📊 **Allure reporting** published to GitHub Pages via CI, plus a 🧹 **ruff** lint/format gate and 🐳 **Docker/Compose** for a reproducible run.

See [Architecture](ARCHITECTURE.md) for the full feature list and the reasoning behind each design choice.

## Verified against a live catalogue drift

This suite runs against the **real, public production** Dulux site, so it occasionally catches real changes: a shade used in the `purchase` test data was found to have been quietly removed from its colour family mid-project, breaking the scenario. The fix, the cross-check against the Java sibling project, and the (rejected) "self-healing" alternative are documented as a materialised risk in the [Test Strategy §10](TEST_STRATEGY.md#10-risk-analysis--mitigations).

## Prerequisites

- **Python 3.12+**
- Internet access (tests run against `dulux.co.uk`)

## Install & run

```bash
python -m venv .venv
.venv/Scripts/activate          # .venv/bin/activate on macOS/Linux
pip install -r requirements.txt
playwright install --with-deps chromium

pytest --collect-only           # confirms scenarios/markers wire up without a browser
pytest -m smoke                 # fast critical-path set
pytest                          # full suite
```

Full marker reference and more CLI examples (cross-browser, headed mode) are in
[Architecture — Tags / markers](ARCHITECTURE.md#tags--markers-reference).

## Run in Docker

```bash
docker compose up --build
PYTEST_MARKERS="regression" docker compose up --build   # a different marker expression
```

Allure results are written back to the host under `./allure-results`.

## Reports

```bash
pytest --alluredir=allure-results
allure serve allure-results
```

In CI, the report is generated automatically and published to GitHub Pages on every push
to `main`.

## Working with the Project (Developer / Tester Guide)

### Project structure

See [Architecture — Project structure](ARCHITECTURE.md#project-structure) for the full
directory layout (`features/`, `pages/`, `support/`, `tests/step_defs/`). In short:

- **`features/*.feature`** — Gherkin scenarios (business-readable, no Playwright code).
- **`tests/step_defs/*.py`** — step definitions binding Gherkin steps to `Context`/page-object calls.
- **`pages/`** — Page Object Model + Component Objects; navigation and interaction only, no assertions.
- **`support/context.py`** — the `Context` class: business-level methods used by step defs, one instance per scenario.
- **`conftest.py`** — `desktop_page` / `tablet_page` / `mobile_page` fixtures (viewport-specific `Page` instances).

### Adding or changing a scenario

1. Write/edit the Gherkin in `features/*.feature` — keep it business-readable, no selectors or technical detail.
2. Add or reuse step definitions in `tests/step_defs/`, calling into `Context` / page objects — never assert inside a page object.
3. Tag the scenario with the relevant `@marker`s (see [Tags / markers reference](ARCHITECTURE.md#tags--markers-reference)) so it's picked up by the right CI workflow.
4. Run it locally before pushing:
   ```bash
   pytest --collect-only              # sanity-check the new step defs wire up
   pytest -k "new_scenario_name" -v
   ```

### Everyday commands

```bash
pytest -m "smoke and desktop" -v           # narrow down by marker + viewport
pytest -k "basket"                         # run scenarios matching a keyword
pytest --headed                            # watch it run in a real browser window
pytest --headed --slowmo 500               # ...and slow it down to actually see it
pytest -m "regression" --browser firefox   # cross-browser (needs `playwright install firefox`/`webkit`)
pytest -x                                  # stop on first failure
```

### Debugging a failing test

```bash
pytest --headed --pdb                      # drop into a debugger on failure, browser stays open
PWDEBUG=1 pytest -k "scenario_name"        # step through with the Playwright Inspector
pytest --tracing on                        # record a Playwright trace (pytest-playwright flag)
playwright show-trace trace.zip            # inspect a recorded trace afterwards
```

Every scenario run also produces an Allure result — `allure serve allure-results` after a
run shows steps, timings and (for the one known-flaky interaction) every retry attempt.

### Linting & formatting

Enforced in CI — run the same checks locally before pushing:

```bash
ruff check .            # lint
ruff check . --fix      # lint, auto-fixing what's safe
ruff format .           # format
ruff format --check .   # format check only (what CI runs)
```

### Git workflow

- Branch off `main` for each change (`feature/…`, `fix/…`, `docs/…`, `chore/…`).
- Open a PR into `main` — the smoke suite + lint run automatically on every push and PR.
- `main` merges trigger the Allure report publish to GitHub Pages.

### Where to look next

- [Features Guide](FEATURES_GUIDE.md) — what each site area under test actually does,
  reverse-engineered from the live site (see [Testing Without Requirements](TESTING_WITHOUT_REQUIREMENTS.md)
  for why that's necessary here).
- [Architecture](ARCHITECTURE.md) — full tech stack, design rationale, a complete sample
  scenario walkthrough, and the tags/markers reference.
- [Test Strategy](TEST_STRATEGY.md) — scope, risk register, coverage gaps, and the
  reasoning behind choices like the allow-listed accessibility violations and the bounded
  retry mechanism.
- [Test Plan](TEST_PLAN.md) — execution-facing scope, schedule, environments and
  entry/exit criteria.
- [Test Cases](TEST_CASES.md) — individual test case specs, automated and manual/candidate.
- [Test Results](TEST_RESULTS.md) / [Test Summary Report](TEST_SUMMARY_REPORT.md) — latest
  known execution status and cycle-level outcome.
- [Lessons Learned](LESSONS_LEARNED.md) — real production incidents this suite has hit
  (catalogue drift, a locator broken by a UI redesign, cross-engine flakiness, a Docker
  image that built but didn't run), each with root cause, fix, and the takeaway.
