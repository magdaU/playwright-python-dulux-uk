# 🏛 Architecture & Design Decisions

> How this framework is built, why it's built that way, and how it compares to its Java
> sibling, [playwright-java-dulux-uk](https://github.com/magdaU/playwright-java-dulux-uk).
> For *what* is tested and *why*, see the [Test Strategy](TEST_STRATEGY.md).

---

## Tech stack

| Tool | Version | Purpose |
|---|---|---|
| Python | 3.12 | Language |
| Playwright | 1.61.0 | Browser automation (Chromium) |
| pytest | 9.1.1 | Test runner |
| pytest-playwright | 0.8.0 | `browser`/`context`/`page` fixtures, `--headed`/`--browser` CLI flags |
| pytest-bdd | 8.1.0 | BDD layer (Gherkin feature files → pytest test items) |
| Allure (`allure-pytest-bdd`) | 2.16.0 | Test reporting with Gherkin step rendering |
| axe-playwright-python | 0.1.8 | Accessibility scanning (`axe-core`) |
| ruff | 0.16.1 | Linting + formatting, enforced in CI |
| Docker / Docker Compose | – | Containerised, reproducible test runs |
| GitHub Actions | – | CI/CD pipeline, GitHub Pages |

> ⚠️ **Don't also install `allure-pytest`** alongside `allure-pytest-bdd` — both register the
> same `--alluredir` CLI option and pytest will refuse to start. See
> [requirements.txt](../requirements.txt).

---

## Why this stack, vs. the Java project

| Concern | Java project | This project | Note |
|---|---|---|---|
| Browser automation | Playwright Java | `playwright` + `pytest-playwright` | `pytest-playwright` supplies fixtures and CLI flags for free — no hand-written `BaseTest` browser lifecycle needed |
| Test runner | JUnit 5 | `pytest` | |
| BDD | Cucumber 7 + PicoContainer DI | `pytest-bdd` | Gherkin `@tag`s become pytest markers automatically — pytest fixtures replace the DI container |
| Assertions | AssertJ | plain `assert` + Playwright `expect()` | pytest rewrites `assert` for rich failure output — no fluent-assertion library needed |
| Reporting | Allure (`allure-junit5` + `allure-cucumber7-jvm`) | `allure-pytest-bdd` | Standalone plugin, single dependency |

Design principles carried over from the Java project: Page Object Model + Component
Objects, no assertions in page objects, role-based locators, web-first waits instead of
sleeps. See the [Test Strategy §4](TEST_STRATEGY.md#4-test-approach) for the full list.

---

## Project structure

```
playwright-python-dulux-uk/
├── requirements.txt
├── pyproject.toml                       # ruff lint + format config
├── pytest.ini                           # markers = pytest equivalent of Cucumber tags
├── conftest.py                          # desktop_page / tablet_page / mobile_page viewport fixtures
├── Dockerfile / docker-compose.yml      # reproducible run, mirrors CI
├── .github/workflows/
│   ├── e2e-tests.yml                    # CI: smoke suite + Allure report + GitHub Pages
│   ├── cross-browser-regression.yml     # on-demand: regression marker across Chromium/Firefox/WebKit
│   └── nightly-regression.yml           # scheduled: regression marker daily against production
├── docs/
│   ├── TEST_STRATEGY.md                 # scope, risk analysis, roadmap
│   └── ARCHITECTURE.md                  # this file
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

## Sample test case, end to end

A real scenario from [`features/tester_purchase.feature`](../features/tester_purchase.feature):

```gherkin
@smoke @desktop
Scenario: Desktop customer adds a tester from the colour finder
  Given a desktop customer starts with an empty basket
  When the customer browses to shade "Violet Morning" from colour family "Violet"
  Then the shade page has no unexpected accessibility violations
  When the customer adds a tester to the basket
  Then the basket contains 1 item
  And the basket includes tester "Dulux Colour Tester" for shade "Violet Morning"
```

...bound to real Playwright actions in
[`tests/step_defs/test_tester_purchase.py`](../tests/step_defs/test_tester_purchase.py):

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


@then("the shade page has no unexpected accessibility violations")
def shade_page_has_no_unexpected_a11y_violations(ctx):
    violations = ctx.get_unexpected_accessibility_violations()
    assert not violations, [f"{v['impact']}:{v['id']}" for v in violations]


@then(parsers.parse("the basket contains {count:d} item"))
def basket_contains_items(ctx, count):
    expect(ctx.cart.get_quantity()).to_have_value(str(count))
```

No `Context` fixture is declared explicitly for the `When`/`Then` steps —
`target_fixture="ctx"` on the `Given` step registers it, and pytest-bdd wires it into every
later step of the same scenario automatically.

---

## Tags / markers reference

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
pytest -m "smoke and desktop"
pytest --headed                            # watch it run in a real browser window
pytest -m "regression" --browser firefox   # or webkit — needs `playwright install firefox`/`webkit` first
```
