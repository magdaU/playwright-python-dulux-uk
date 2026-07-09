# playwright-python-dulux-uk

Python port of [playwright-java-dulux-uk](https://github.com/magdaU/playwright-java-dulux-uk) — same Dulux UK journeys (buy a colour tester, open the Visualizer), same Page Object Model + BDD architecture, Python ecosystem instead of Java.

**Status:** implemented and verified against the live site — all 4 scenarios pass (`pytest -m smoke`/`regression`, desktop + mobile). The `purchase` scenarios originally used the shade "Gentle Lavender", which turned out to have been removed from the "Violet" family on production (confirmed by the identical scenario failing in [playwright-java-dulux-uk](https://github.com/magdaU/playwright-java-dulux-uk) too — see the [Test Strategy](docs/TEST_STRATEGY.md#10-risk-analysis--mitigations) risk log). Test data was refreshed to "Violet Morning".

> 🧭 **New here?** Read the [**Test Strategy**](docs/TEST_STRATEGY.md) — what we test, why, the scope, risk analysis and the roadmap.

## Why this stack

| Concern | Java project | This project | Note |
|---|---|---|---|
| Browser automation | Playwright Java | `playwright` + `pytest-playwright` | `pytest-playwright` supplies `browser`/`context`/`page` fixtures and `--headed`/`--browser` CLI flags for free — no hand-written `BaseTest` browser lifecycle needed |
| Test runner | JUnit 5 | `pytest` | |
| BDD | Cucumber 7 + PicoContainer DI | `pytest-bdd` | Gherkin `@tag`s become pytest markers automatically — no separate DI container needed, pytest fixtures fill that role |
| Assertions | AssertJ | plain `assert` | pytest rewrites `assert` statements for rich failure output, so no fluent-assertion library is needed |
| Reporting | Allure (`allure-junit5` + `allure-cucumber7-jvm`) | `allure-pytest-bdd` | Standalone plugin — do **not** also install `allure-pytest`, both register the same `--alluredir` CLI option and pytest refuses to start |

## Structure

```
├── requirements.txt
├── pytest.ini                          # markers = pytest equivalent of Cucumber tags
├── conftest.py                         # desktop_page / mobile_page viewport fixtures
├── Dockerfile / docker-compose.yml     # reproducible run, mirrors CI
├── .github/workflows/e2e-tests.yml     # CI: smoke suite + Allure report + GitHub Pages
├── docs/
│   └── TEST_STRATEGY.md
├── features/
│   ├── tester_purchase.feature         # ported as-is (Gherkin is language-agnostic)
│   └── visualizer_experience.feature
├── pages/
│   ├── base_page.py
│   ├── home_page.py
│   ├── color_selection_page.py
│   ├── cart_page.py
│   └── components/
│       ├── navigation_component.py
│       └── alert_component.py
└── tests/
    └── step_defs/
        ├── test_tester_purchase.py
        └── test_visualizer_experience.py
```

## Getting started

```bash
python -m venv .venv
.venv/Scripts/activate        # .venv/bin/activate on macOS/Linux
pip install -r requirements.txt
playwright install --with-deps chromium

pytest --collect-only         # confirms scenarios/markers wire up without a browser
pytest -m smoke                # runs the fast critical-path set
```
