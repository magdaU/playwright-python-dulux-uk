# ✅ Test Cases

> Individual test case specifications — the automated ones map 1:1 to the Gherkin
> scenarios in [`features/`](../features/) (§3.1 of the [Test Strategy](TEST_STRATEGY.md#31-test-scenarios-implemented));
> a further set are documented as **manual/candidate** cases that close gaps identified in
> [Test Strategy §14](TEST_STRATEGY.md#14-coverage-gaps--improvement-opportunities) but
> aren't automated today. See the [Features Guide](FEATURES_GUIDE.md) for what each area
> under test actually does.

**Legend — Priority:** P1 critical path · P2 important · P3 nice-to-have.
**Legend — Automation:** ✅ automated (linked) · 🟡 candidate for automation · ⚪ manual/exploratory only.

---

## Purchase journey

### TC-01 — Desktop customer adds a tester from the colour finder
| | |
|---|---|
| **Priority** | P1 |
| **Automation** | ✅ [`tester_purchase.feature` — Scenario 1](../features/tester_purchase.feature) |
| **Preconditions** | Desktop viewport (`1920×1080`); basket is empty; cookie banner not yet dismissed |
| **Steps** | 1. Open the home page and reject cookies.<br>2. Open "Find a colour" from the top nav.<br>3. Select colour family "Violet".<br>4. Select shade "Violet Morning".<br>5. Click "Buy a Tester in this colour".<br>6. Dismiss the confirmation alert.<br>7. Open the shopping cart. |
| **Expected result** | Shade page has no unexpected accessibility violations; basket contains exactly 1 item; basket shows tester "Dulux Colour Tester" for shade "Violet Morning" |

### TC-02 — Tablet customer adds a tester from the colour finder
| | |
|---|---|
| **Priority** | P2 |
| **Automation** | ✅ [`tester_purchase.feature` — Scenario 2](../features/tester_purchase.feature) |
| **Preconditions** | Tablet viewport (`768×1024`); basket is empty |
| **Steps** | Same as TC-01, but "Find a colour" is reached via the hamburger menu, not the top nav |
| **Expected result** | Same as TC-01 |

### TC-03 — Mobile customer adds a tester from the colour finder
| | |
|---|---|
| **Priority** | P2 |
| **Automation** | ✅ [`tester_purchase.feature` — Scenario 3](../features/tester_purchase.feature) |
| **Preconditions** | Mobile viewport (`375×667`); basket is empty |
| **Steps** | Same as TC-02 (hamburger-menu navigation) |
| **Expected result** | Same as TC-01 |

### TC-04 — Basket increment/decrement/remove *(manual/candidate)*
| | |
|---|---|
| **Priority** | P2 |
| **Automation** | 🟡 candidate — see [Test Strategy §14](TEST_STRATEGY.md#14-coverage-gaps--improvement-opportunities) |
| **Preconditions** | Basket already contains 1 tester (result of TC-01) |
| **Steps** | 1. Increase quantity by 1 via the spinbutton.<br>2. Decrease quantity back to 1.<br>3. Remove the item entirely. |
| **Expected result** | Quantity updates correctly at each step; basket shows the "empty" state after removal |

### TC-05 — Add-to-basket failure is surfaced to the customer *(manual/candidate)*
| | |
|---|---|
| **Priority** | P2 |
| **Automation** | 🟡 candidate — via `page.route()` interception, see [Test Strategy §14](TEST_STRATEGY.md#14-coverage-gaps--improvement-opportunities) |
| **Preconditions** | Customer is on a shade page; the add-to-basket network call can be intercepted |
| **Steps** | 1. Force the add-to-basket request to fail (mocked error response).<br>2. Click "Buy a Tester in this colour". |
| **Expected result** | The customer sees a visible error/failure indication — not a silent no-op |

### TC-06 — Shade with no tester option *(manual/exploratory)*
| | |
|---|---|
| **Priority** | P3 |
| **Automation** | ⚪ manual — data-dependent on which shades currently lack a tester |
| **Preconditions** | A shade known to expose only "Find Products in this colour", no "Buy a Tester" button (e.g. "Cotton Breeze" under "Violet" at time of writing — catalogue can drift, see [Lessons Learned #1](LESSONS_LEARNED.md#1-product-catalogue-drift--a-pinned-shade-disappeared-from-its-colour-family)) |
| **Steps** | 1. Navigate to that shade's page.<br>2. Confirm no "Buy a Tester" control is present. |
| **Expected result** | Confirms the assumption behind the pinned-shade decision still holds; re-run whenever choosing a new pinned shade |

---

## Visualizer journey

### TC-07 — Desktop customer opens the Visualizer for a shade
| | |
|---|---|
| **Priority** | P1 |
| **Automation** | ✅ [`visualizer_experience.feature` — Scenario 1](../features/visualizer_experience.feature) |
| **Preconditions** | Desktop viewport; customer is viewing shade "Gentle Lavender" (reached via search) |
| **Steps** | 1. Click "Try our Visualizer App". |
| **Expected result** | Visualizer opens in a **new browser tab**, at `https://www.dulux.co.uk/en/articles/dulux-visualizer-app` |

### TC-08 — Mobile customer tries to open the Visualizer for a shade
| | |
|---|---|
| **Priority** | P2 |
| **Automation** | ✅ [`visualizer_experience.feature` — Scenario 2](../features/visualizer_experience.feature) |
| **Preconditions** | Mobile viewport; customer is viewing shade "Gentle Lavender" |
| **Steps** | 1. Click "Try our Visualizer App". |
| **Expected result** | No new tab; the page shows the message "Inconsistent store data, contact support@adjust.com" — documented, observed behaviour (see [Features Guide](FEATURES_GUIDE.md#visualizer-app)) |

---

## Navigation & search

### TC-09 — Site search returns the searched shade *(manual/candidate)*
| | |
|---|---|
| **Priority** | P2 |
| **Automation** | 🟡 candidate — `search_for_shade()` already exists in `Context` and is exercised as setup in TC-07/TC-08, but has no dedicated scenario asserting *search itself* works for an arbitrary term |
| **Preconditions** | On the home page |
| **Steps** | 1. Open search.<br>2. Enter a known shade name.<br>3. Press Enter. |
| **Expected result** | Navigates to that shade's detail page |

### TC-10 — Cookie banner blocks interaction until dismissed *(manual/exploratory)*
| | |
|---|---|
| **Priority** | P3 |
| **Automation** | ⚪ manual — implicitly covered by every scenario rejecting cookies first, but never asserted as a standalone case |
| **Preconditions** | Fresh browser context, cookie banner not yet interacted with |
| **Steps** | 1. Attempt to interact with the page behind the banner before dismissing it. |
| **Expected result** | The banner blocks the intended interaction until "Reject All" (or equivalent) is clicked |

---

## Accessibility

### TC-11 — Shade page has no *new* critical/serious accessibility violations
| | |
|---|---|
| **Priority** | P1 |
| **Automation** | ✅ embedded as a step in TC-01/TC-02/TC-03 (`support/accessibility.py`) |
| **Preconditions** | Shade page loaded (desktop or mobile) |
| **Steps** | 1. Run an `axe-core` scan against the page. |
| **Expected result** | No violation with an ID outside the documented allow-list (`image-alt`, `color-contrast` on desktop; `image-alt`, `color-contrast`, `label` on mobile) |

---

## See also

- [Test Strategy §3.1](TEST_STRATEGY.md#31-test-scenarios-implemented) — scenario-level tags and viewport matrix.
- [Test Results](TEST_RESULTS.md) — latest execution status per test case.
- [Test Summary Report](TEST_SUMMARY_REPORT.md) — cycle-level outcome and sign-off.
