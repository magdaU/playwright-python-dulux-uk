# 🧩 Features Guide

> A functional walkthrough of the Dulux UK areas this suite exercises — written from the
> outside, by exploring the live site, since no internal spec or design doc is available
> for a third-party production site (see [Testing Without Requirements](TESTING_WITHOUT_REQUIREMENTS.md)
> for the approach behind that). This is the closest thing this project has to a functional
> spec, and it doubles as an onboarding map: where each feature lives in the code is noted
> alongside what it does.

---

## Home page & cookie consent

**What it is:** `https://www.dulux.co.uk` — the entry point for every journey.

**Key behaviour:**
- A cookie-consent banner (OneTrust) blocks interaction with the rest of the page until
  dismissed. Every scenario rejects it first (`reject_all_cookies()` — `#onetrust-reject-all-handler`).
- Hosts the global navigation (see below).

**Code:** [`pages/home_page.py`](../pages/home_page.py)

---

## Global navigation

**What it is:** the top-level nav, present on every page, with different affordances per
viewport.

**Key behaviour:**
- **Desktop** exposes a visible top nav bar, including a **"Find a colour"** entry.
- **Tablet (`768×1024`) and mobile (`375×667`)** collapse the same nav behind a **hamburger
  ("Menu")** button — confirmed against production that the responsive breakpoint sits
  between `1024px` and `1280px`, so tablet portrait uses the same interaction path as
  mobile, not the desktop one.
- **"Find a colour"** triggers a **full page navigation**, not a dropdown/panel — a real
  gotcha: the click needs a `wait_for_load_state()` before the next interaction, or it
  resolves against the outgoing page.
- A **search box** (`search-field`) accepts free text and submits on Enter — used to jump
  directly to a known shade page without walking the colour-family tree.
- A **Shopping Cart** link opens the basket.

**Code:** [`pages/components/navigation_component.py`](../pages/components/navigation_component.py)

---

## Find a Colour / colour finder

**What it is:** the family → shade drill-down reached via **"Find a colour"**.

**Key behaviour:**
- Colour **families** (e.g. "Violet") and individual **shades** (e.g. "Violet Morning")
  are each rendered as a named button — selected via `get_by_role("button", name=...)`.
- Not every shade offers the same actions further down the funnel (see the shade page,
  below) — this was discovered while investigating a "self-healing" shade-selection
  alternative (see [Lessons Learned #1](LESSONS_LEARNED.md#1-product-catalogue-drift--a-pinned-shade-disappeared-from-its-colour-family)):
  the catalogue's first-listed shade under "Violet" ("Cotton Breeze") had no tester
  purchase option at all.
- This interaction is the one place a genuine, engine-specific timing difference has been
  observed on Firefox/WebKit (not a bug in the site, a real cross-browser difference) — see
  [Lessons Learned #3](LESSONS_LEARNED.md#3-cross-engine-navigation-timing--the-same-interaction-behaves-differently-per-browser-engine).

**Code:** [`pages/color_selection_page.py`](../pages/color_selection_page.py) (`choose_colour`, `choose_shade`)

---

## Shade / colour detail page

**What it is:** the page for one specific shade, reached either via the colour finder or
directly via search.

**Key actions available on this page:**
- **"Buy a Tester in this colour"** — adds a tester for this shade to the basket and shows
  a dismissible confirmation alert (`get_by_role("alert")`).
- **"Try our Visualizer App"** (a list item containing a link) — opens the Visualizer
  experience. **On desktop** this opens in a genuinely new browser tab (captured via
  Playwright's `expect_page()`); **on mobile** it does not — see Visualizer, below.

**Accessibility:** this page carries known, pre-existing production a11y issues
(`image-alt`, `color-contrast` on desktop; also `label` on mobile) that are scanned for on
every purchase-journey run and allow-listed by ID rather than gated on — see
[Lessons Learned #4](LESSONS_LEARNED.md#4-pre-existing-accessibility-violations-on-a-site-we-dont-own).

**Code:** [`pages/color_selection_page.py`](../pages/color_selection_page.py), [`support/accessibility.py`](../support/accessibility.py)

---

## Basket / Cart

**What it is:** `https://www.dulux.co.uk/en/store/cart` — where an added tester shows up.

**Key behaviour:**
- An **empty basket** shows the literal text "Your basket is empty".
- Once an item is added, a **quantity control** is present — exposed as an accessible
  `spinbutton` labelled "Quantity input". This control was redesigned mid-project into a
  `group` wrapping three elements that all mention "Quantity" in their accessible name,
  breaking a looser, substring-based locator — see
  [Lessons Learned #2](LESSONS_LEARNED.md#2-basket-ui-markup-drift--a-redesign-broke-a-locators-uniqueness-not-its-match).
- The basket lists the **tester's product name** and the **shade name** as plain text.
- No transaction ever completes against production — the suite verifies basket *state*,
  never checkout.

**Code:** [`pages/cart_page.py`](../pages/cart_page.py)

---

## Visualizer app

**What it is:** a third-party (Adjust-powered) app letting a customer preview a colour,
launched from a shade's detail page.

**Key behaviour — genuinely different per viewport, not a bug in either case:**
- **Desktop:** opens in a **new browser tab**, at a fixed, documented URL
  (`https://www.dulux.co.uk/en/articles/dulux-visualizer-app`).
- **Mobile:** does **not** open the app — instead the page shows the literal message
  `"Inconsistent store data, contact support@adjust.com"` inside a `<pre>` element. This is
  asserted as observed, documented behaviour, not assumed to be either correct or a defect
  — see [Testing Without Requirements](TESTING_WITHOUT_REQUIREMENTS.md) for why that
  distinction matters when there's no spec to confirm intent against.

**Code:** `open_visualizer_experience()` in [`support/context.py`](../support/context.py)

---

## See also

- [Test Strategy §3.1](TEST_STRATEGY.md#31-test-scenarios-implemented) — the automated
  scenarios that exercise these features today.
- [Test Cases](TEST_CASES.md) — individual test case specifications, automated and manual.
- [Architecture](ARCHITECTURE.md) — how these page objects fit into the framework.
