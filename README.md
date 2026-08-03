<div align="center">

# 🐍 Playwright Python E2E Automation Framework

### UI end-to-end test automation for [Dulux UK](https://www.dulux.co.uk) — Python · Playwright · pytest-bdd · Allure · CI/CD

[![E2E Tests](https://github.com/magdaU/playwright-python-dulux-uk/actions/workflows/e2e-tests.yml/badge.svg)](https://github.com/magdaU/playwright-python-dulux-uk/actions/workflows/e2e-tests.yml)
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

Python port of [playwright-java-dulux-uk](https://github.com/magdaU/playwright-java-dulux-uk) — the **same** real Dulux UK customer journeys (buy a colour tester, launch the Visualizer app), the **same** Page Object Model + BDD architecture, a different stack. Where the Java version reaches for Cucumber + PicoContainer DI, this one leans on `pytest-bdd` + plain pytest fixtures — idiomatic Python, not a line-by-line transliteration.

> **Status:** implemented and verified against production — all 5 scenarios pass (desktop + tablet + mobile `purchase`, desktop + mobile `visualizer`). See [Verified against a live catalogue drift](#-verified-against-a-live-catalogue-drift) below for a real example of this suite catching (and adapting to) a production data change.

> 🧭 **New here?** Read the [**Test Strategy**](docs/TEST_STRATEGY.md) — what we test, why, the scope, risk analysis and the roadmap.

---

## ✨ Key Features

- 🧱 **Page Object Model + Component Objects** — `HomePage`, `ColorSelectionPage`, `CartPage` and reusable components (`NavigationComponent`, `AlertComponent`) each extend a shared `BasePage`.
- 🥒 **BDD with pytest-bdd** — scenarios written in plain-language Gherkin; `@tag`s become pytest markers automatically, filterable with `-m "smoke"` etc. — no separate tag-mapping config needed.
- 📱 **Cross-viewport coverage** — `purchase` runs at desktop (`1920×1080`), tablet (`768×1024`) and mobile (`375×667`); `visualizer` at desktop and mobile — via dedicated `desktop_page` / `tablet_page` / `mobile_page` fixtures.
- 🪶 **No DI container needed** — `pytest-bdd`'s `target_fixture` binds a `Context` object (business methods + page objects) to each scenario from its `Given` step; later steps just request it as a fixture. The Python-idiomatic equivalent of the Java project's PicoContainer setup.
- ✅ **Assertions in the test layer only** — page objects never assert; plain `assert` + Playwright's web-first `expect()` live in the step layer.
- 📊 **Allure reporting** (`allure-pytest-bdd`) — Gherkin steps rendered per scenario, published to GitHub Pages via CI.
- 🚀 **CI/CD with GitHub Actions** — smoke suite on every push/PR, Allure report generated and uploaded as an artifact.
- 🌙 **Nightly regression** — [`nightly-regression.yml`](.github/workflows/nightly-regression.yml) runs the full `regression` suite against production daily (02:00 UTC), independent of any push, to catch drift on days with no code changes.
- 🌐 **Cross-browser regression** — Chromium, Firefox and WebKit via `pytest --browser <name>`; wired into an on-demand [`cross-browser-regression.yml`](.github/workflows/cross-browser-regression.yml) workflow (matrix job) so the push/PR gate stays fast and Chromium-only.
- ♿ **Accessibility scanning** — `axe-core` (via `axe-playwright-python`) checks the shade page in both `purchase` scenarios; known, pre-existing production violations are allow-listed by ID (`support/accessibility.py`) so the suite still fails on *new* critical/serious issues without gating on defects we don't own.
- 🔁 **Bounded, reported retries** — `support/retry.py` retries the one interaction identified as genuinely flaky across browser engines, up to 3 attempts; every attempt is logged and attached to the Allure report, so a retried pass is never silently indistinguishable from a clean one.
- 🐳 **Docker / Docker Compose** — reproducible run matching CI, mirrors the Java project's container setup.

---

## 🧰 Tech Stack

| Tool | Version | Purpose |
|---|---|---|
| Python | 3.12 | Language |
| Playwright | 1.61.0 | Browser automation (Chromium) |
| pytest | 9.1.1 | Test runner |
| pytest-playwright | 0.8.0 | `browser`/`context`/`page` fixtures, `--headed`/`--browser` CLI flags |
| pytest-bdd | 8.1.0 | BDD layer (Gherkin feature files → pytest test items) |
| Allure (`allure-pytest-bdd`) | 2.16.0 | Test reporting with Gherkin step rendering |
| axe-playwright-python | 0.1.8 | Accessibility scanning (`axe-core`) |
| Docker / Docker Compose | – | Containerised, reproducible test runs |
| GitHub Actions | – | CI/CD pipeline, GitHub Pages |

> ⚠️ **Don't also install `allure-pytest`** alongside `allure-pytest-bdd` — both register the same `--alluredir` CLI option and pytest will refuse to start. See [requirements.txt](requirements.txt).

---

## 🏛 Why this stack (vs. the Java project)

| Concern | Java project | This project | Note |
|---|---|---|---|
| Browser automation | Playwright Java | `playwright` + `pytest-playwright` | `pytest-playwright` supplies fixtures and CLI flags for free — no hand-written `BaseTest` browser lifecycle needed |
| Test runner | JUnit 5 | `pytest` | |
| BDD | Cucumber 7 + PicoContainer DI | `pytest-bdd` | Gherkin `@tag`s become pytest markers automatically — pytest fixtures replace the DI container |
| Assertions | AssertJ | plain `assert` + Playwright `expect()` | pytest rewrites `assert` for rich failure output — no fluent-assertion library needed |
| Reporting | Allure (`allure-junit5` + `allure-cucumber7-jvm`) | `allure-pytest-bdd` | Standalone plugin, single dependency |

---

## 🗂 Project Structure

```
playwright-python-dulux-uk/
├── requirements.txt
├── pytest.ini                          # markers = pytest equivalent of Cucumber tags
├── conftest.py                          # desktop_page / tablet_page / mobile_page viewport fixtures
├── Dockerfile / docker-compose.yml      # reproducible run, mirrors CI
├── .github/workflows/e2e-tests.yml      # CI: smoke suite + Allure report + GitHub Pages
├── docs/
│   └── TEST_STRATEGY.md                 # scope, risk analysis, roadmap
├── features/
│   ├── tester_purchase.feature          # ported as-is (Gherkin is language-agnostic)
│   └── visualizer_experience.feature
├── pages/
│   ├── base_page.py                     # shared `page` handle
│   ├── home_page.py                     # navigate, reject cookies
│   ├── color_selection_page.py          # choose colour family / shade, buy tester, open Visualizer
│   ├── cart_page.py                     # basket state + assertions targets
│   └── components/
│       ├── navigation_component.py      # top nav, hamburger menu, search
│       └── alert_component.py           # "added to basket" confirmation
├── support/
│   ├── context.py                       # Context: business methods + page objects per scenario
│   ├── accessibility.py                 # axe-core scan + allow-listed known violation IDs
│   └── retry.py                         # bounded, reported retry for known-flaky steps
└── tests/
    └── step_defs/
        ├── test_tester_purchase.py
        └── test_visualizer_experience.py
```

---

## 🧪 Sample test case

A real scenario from [`features/tester_purchase.feature`](features/tester_purchase.feature):

```gherkin
@smoke @desktop
Scenario: Desktop customer adds a tester from the colour finder
  Given a desktop customer starts with an empty basket
  When the customer browses to shade "Violet Morning" from colour family "Violet"
  And the customer adds a tester to the basket
  Then the basket contains 1 item
  And the basket includes tester "Dulux Colour Tester" for shade "Violet Morning"
```

...bound to real Playwright actions in [`tests/step_defs/test_tester_purchase.py`](tests/step_defs/test_tester_purchase.py):

```python
@given("a desktop customer starts with an empty basket", target_fixture="ctx")
def desktop_empty_basket(desktop_page):
    ctx = Context(page=desktop_page, desktop=True)
    ctx.open_empty_cart()
    expect(ctx.cart.get_basket_empty_text()).to_be_visible()
    return ctx


@when(parsers.parse('the customer browses to shade "{shade}" from colour family "{colour_family}"'))
def browse_to_shade(ctx, shade, colour_family):
    ctx.browse_to_shade(colour_family, shade, mobile_navigation=False)


@then(parsers.parse("the basket contains {count:d} item"))
def basket_contains_items(ctx, count):
    expect(ctx.cart.get_quantity()).to_have_value(str(count))
```

No `Context` fixture is declared explicitly for the `When`/`Then` steps — `target_fixture="ctx"` on the `Given` step registers it, and pytest-bdd wires it into every later step of the same scenario automatically.

---

## 🎯 Verified against a live catalogue drift

This suite runs against the **real, public production** Dulux site — which means it occasionally catches real changes. While implementing the `purchase` journey, the shade originally used in the test data ("Gentle Lavender") turned out to have been quietly removed from the "Violet" family's default listing. The scenario started timing out waiting for a button that no longer existed.

To confirm this was a production data drift and not a bug in this port, the **identical scenario was run in the Java sibling project** — it failed the exact same way. Test data was refreshed to a shade confirmed present in the catalogue ("Violet Morning"), and the incident is documented as a materialised risk in the [Test Strategy](docs/TEST_STRATEGY.md#10-risk-analysis--mitigations) rather than quietly patched over.

A "self-healing" fix (auto-pick whichever shade is listed first) was investigated and deliberately **rejected**: not every shade in the catalogue has a tester available for direct purchase, so picking an arbitrary one isn't actually more reliable than a pinned, verified name. See §13 of the Test Strategy for the full reasoning.

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

### Tags / markers

| Marker | Meaning |
|---|---|
| `smoke` | Fast critical-path set — desktop-only, both journeys |
| `regression` | Full journey coverage |
| `desktop` | Desktop-viewport (`1920×1080`) scenarios |
| `tablet` | Tablet-viewport (`768×1024`) scenarios |
| `mobile` | Mobile-viewport (`375×667`) scenarios |
| `purchase` | Tester purchase journey |
| `visualizer` | Visualizer experience journey |

```bash
pytest -m "smoke"
pytest -m "regression"
pytest -m "desktop"
pytest -m "smoke and desktop"
pytest --headed                 # watch it run in a real browser window

pytest -m "regression" --browser firefox   # or webkit — needs `playwright install firefox`/`webkit` first
```

---

## 🐳 Run in Docker

```bash
# Build the image and run the smoke suite
docker compose up --build

# Run a different marker expression
PYTEST_MARKERS="regression" docker compose up --build
```

Allure results are written back to the host under `./allure-results`.

---

## 📊 Reports

```bash
pytest --alluredir=allure-results     # run tests → write Allure results
allure generate allure-results --clean -o allure-report
allure serve allure-results           # or serve the report directly
```

In CI, the report is generated automatically and published to GitHub Pages on every push to `main` — see [`.github/workflows/e2e-tests.yml`](.github/workflows/e2e-tests.yml).

---

## 👩‍💻 Author

**Magdalena Ukleja**

[![GitHub](https://img.shields.io/badge/GitHub-magdaU-181717?logo=github&logoColor=white)](https://github.com/magdaU)

QA Automation Engineer — Python · Java · Playwright · BDD · CI/CD.
