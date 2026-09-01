<div align="center">

# 🐍 Playwright Python E2E Automation Framework

### UI end-to-end test automation for [Dulux UK](https://www.dulux.co.uk) — Python · Playwright · pytest-bdd · Allure · CI/CD

[![E2E Tests](https://github.com/magdaU/playwright-python-dulux-uk/actions/workflows/e2e-tests.yml/badge.svg)](https://github.com/magdaU/playwright-python-dulux-uk/actions/workflows/e2e-tests.yml)
[![Cross-Browser Regression](https://github.com/magdaU/playwright-python-dulux-uk/actions/workflows/cross-browser-regression.yml/badge.svg)](https://github.com/magdaU/playwright-python-dulux-uk/actions/workflows/cross-browser-regression.yml)
[![Nightly Regression](https://github.com/magdaU/playwright-python-dulux-uk/actions/workflows/nightly-regression.yml/badge.svg)](https://github.com/magdaU/playwright-python-dulux-uk/actions/workflows/nightly-regression.yml)
[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Playwright](https://img.shields.io/badge/Playwright-1.61-2EAD33?logo=playwright&logoColor=white)](https://playwright.dev/python/)
[![pytest](https://img.shields.io/badge/pytest-9.1-0A9EDC?logo=pytest&logoColor=white)](https://docs.pytest.org/)
[![pytest-bdd](https://img.shields.io/badge/pytest--bdd-8.1-0A9EDC?logo=cucumber&logoColor=white)](https://pytest-bdd.readthedocs.io/)
[![Allure](https://img.shields.io/badge/Allure-Report-brightgreen?logo=qameta&logoColor=white)](https://github.com/magdaU/playwright-python-dulux-uk/actions/workflows/e2e-tests.yml)
[![Test Strategy](https://img.shields.io/badge/Test-Strategy-8A2BE2?logo=readthedocs&logoColor=white)](docs/TEST_STRATEGY.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

</div>

---

## 📖 Overview

Python port of [playwright-java-dulux-uk](https://github.com/magdaU/playwright-java-dulux-uk) — the **same** real Dulux UK customer journeys (buy a colour tester, launch the Visualizer app), the **same** Page Object Model + BDD architecture, a different stack (`pytest-bdd` + plain pytest fixtures instead of Cucumber + PicoContainer DI).

> **Status:** implemented and verified against production — all 5 scenarios pass (desktop + tablet + mobile `purchase`, desktop + mobile `visualizer`).

📚 **Docs:** [Test Strategy](docs/TEST_STRATEGY.md) (what we test, why, scope, risk analysis, roadmap) · [Architecture](docs/ARCHITECTURE.md) (tech stack, design rationale, project structure, a full sample scenario walkthrough).

---

## 🎓 What This Project Demonstrates

This isn't a toy TODO-app suite — it's built against a real, live production e-commerce
site, which surfaces the same problems a professional QA/SDET role deals with day to day:

- **Risk-based test strategy, not just test scripts** — [Test Strategy](docs/TEST_STRATEGY.md)
  defines scope with explicit trade-offs (what's deliberately *out*, and why), a
  prioritised risk register, and entry/exit criteria — the kind of document a team lead
  reviews before trusting a suite's "green".
- **Real bugs found and triaged, not simulated ones** — this suite has caught genuine
  production issues while it was being built: a colour shade quietly removed from its
  family (catalogue drift), a basket control redesign that broke a locator's uniqueness,
  and a genuine cross-browser navigation-timing difference. Each is root-caused and
  documented in [Test Strategy §10](docs/TEST_STRATEGY.md#10-risk-analysis--mitigations)
  rather than papered over with a blanket retry.
- **Judgement calls, documented** — e.g. "self-healing" shade selection and visual
  regression were both seriously considered and **deliberately rejected** for now, with the
  reasoning kept in the roadmap ([§13](docs/TEST_STRATEGY.md#13-maintenance--roadmap))
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
  [Test Strategy §13](docs/TEST_STRATEGY.md#13-maintenance--roadmap).
- **Stack-agnostic QA design** — the same architecture and strategy exist in
  [a Java/Cucumber sibling project](https://github.com/magdaU/playwright-java-dulux-uk),
  showing this is a transferable way of thinking about test design, not a one-language trick.

---

## ✨ Key Features

- 🧱 **Page Object Model + Component Objects**, no assertions in page objects — all `expect()`/`assert` calls live in the step layer.
- 🥒 **BDD with pytest-bdd** — Gherkin `@tag`s become pytest markers automatically, filterable with `-m "smoke"` etc.
- 📱 **Cross-viewport coverage** — `purchase` at desktop/tablet/mobile, `visualizer` at desktop/mobile, via dedicated viewport fixtures.
- ♿ **Accessibility scanning** — `axe-core` on the shade page; known pre-existing production violations are allow-listed by ID so the suite still catches *new* ones.
- 🔁 **Bounded, reported retries** for the one interaction identified as genuinely flaky across browser engines — every attempt logged and attached to the Allure report.
- 🌐 **Cross-browser & nightly regression** — Chromium/Firefox/WebKit on demand, full regression suite scheduled daily against production.
- 📊 **Allure reporting** published to GitHub Pages via CI, plus a 🧹 **ruff** lint/format gate and 🐳 **Docker/Compose** for a reproducible run.

See [Architecture](docs/ARCHITECTURE.md) for the full feature list and the reasoning behind each design choice.

---

## 🎯 Verified against a live catalogue drift

This suite runs against the **real, public production** Dulux site, so it occasionally catches real changes: a shade used in the `purchase` test data was found to have been quietly removed from its colour family mid-project, breaking the scenario. The fix, the cross-check against the Java sibling project, and the (rejected) "self-healing" alternative are documented as a materialised risk in the [Test Strategy §10](docs/TEST_STRATEGY.md#10-risk-analysis--mitigations).

---

## 🚀 Getting Started

### Prerequisites
- **Python 3.12+**
- Internet access (tests run against `dulux.co.uk`)

### Install & run

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
[Architecture — Tags / markers](docs/ARCHITECTURE.md#tags--markers-reference).

### Run in Docker

```bash
docker compose up --build
PYTEST_MARKERS="regression" docker compose up --build   # a different marker expression
```

Allure results are written back to the host under `./allure-results`.

### Reports

```bash
pytest --alluredir=allure-results
allure serve allure-results
```

In CI, the report is generated automatically and published to GitHub Pages on every push
to `main`. A real run of the full suite, rendered locally from this repo's own Allure
output:

![Allure report dashboard — 5 test cases, 100% pass rate](docs/assets/allure-dashboard.png)

---

## 👩‍💻 Author

**Magdalena Ukleja**

[![GitHub](https://img.shields.io/badge/GitHub-magdaU-181717?logo=github&logoColor=white)](https://github.com/magdaU)

QA Automation Engineer — Python · Java · Playwright · BDD · CI/CD.
