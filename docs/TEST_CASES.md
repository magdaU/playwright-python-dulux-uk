# ✅ Test Cases

> Individual test case specifications — the automated ones map 1:1 to the Gherkin
> scenarios in [`features/`](../features/) (§3.1 of the [Test Strategy](TEST_STRATEGY.md#31-test-scenarios-implemented));
> a further set are documented as **manual/candidate** cases that close gaps identified in
> [Test Strategy §14](TEST_STRATEGY.md#14-coverage-gaps--improvement-opportunities) but
> aren't automated today. See the [Features Guide](FEATURES_GUIDE.md) for what each area
> under test actually does.

**Legend — Priority:** P1 critical path · P2 important · P3 nice-to-have. The Priority of an
automated case also sets that test's **severity** in the Allure report (P1 → critical, P2 → normal,
P3 → minor) — `support/allure_metadata.py` reads it from this file, so changing it here changes the report.
**Legend — Automation:** ✅ automated (linked) · 🟡 candidate for automation · ⚪ manual/exploratory only.

---

## Purchase journey

### TC-01 — Desktop customer adds a tester from the colour finder
| | |
|---|---|
| **Priority** | P1 |
| **Automation** | ✅ [`tester_purchase.feature` — Scenario 1](../features/tester_purchase.feature) |
| **Preconditions** | Desktop viewport (`1920×1080`); basket is empty; cookie banner not yet dismissed |
| **Steps** | 1. Open the home page and reject cookies.<br>2. Open "Find a colour" from the top nav.<br>3. Select colour family "Violet".<br>4. Select shade "Romantic Reverie".<br>5. Click "Buy a Tester in this colour".<br>6. Dismiss the confirmation alert.<br>7. Open the shopping cart. |
| **Expected result** | Shade page has no unexpected accessibility violations; basket contains exactly 1 item; basket shows tester "Dulux Colour Tester" for shade "Romantic Reverie" |

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

### TC-04a — Tester quantity boundary values
| | |
|---|---|
| **Priority** | P2 |
| **Automation** | ✅ [`tester_purchase.feature` — Scenario Outline "changes the tester quantity at its boundaries"](../features/tester_purchase.feature) |
| **Preconditions** | Desktop viewport (`1920×1080`); basket contains 1 tester (result of TC-01's steps) |
| **Steps** | Enter each value into the basket quantity field and tab out: `1`, `23`, `0`, `24` |
| **Expected result** | `1` → 1 and `23` → 23 are accepted. `0` and `24` are rejected and the field settles back on the last accepted quantity (1). Behaviour observed on production 2026-10-08: the field's HTML declares `min=1 max=999`, but the server (`POST /store/api/order`) rejects quantities above 23 with HTTP 422 |
| **Note** | The 23 limit is server-side and not documented; if the retailer changes it, the `23`/`24` rows need updating (same catalogue-drift risk as the pinned shade) |

### TC-04 — Basket increment/decrement/remove
| | |
|---|---|
| **Priority** | P2 |
| **Automation** | ✅ [`tester_purchase.feature` — "Desktop customer changes the basket quantity and removes the tester"](../features/tester_purchase.feature) |
| **Preconditions** | Basket already contains 1 tester (the TC-01 steps) |
| **Steps** | 1. Click "Increase quantity" (+).<br>2. Click "Decrease quantity" (−).<br>3. Click the remove (bin) button. |
| **Expected result** | Quantity goes 1 → 2 → 1; the − button is disabled at 1 (the minimum); after removal the basket shows "Your basket is empty" |

### TC-05 — Add-to-basket failure is surfaced to the customer
| | |
|---|---|
| **Priority** | P2 |
| **Automation** | ✅ [`tester_purchase.feature` — "Desktop customer is told when adding a tester to the basket fails"](../features/tester_purchase.feature) (`@negative`) — the request is stubbed with `page.route()`, so the failure never reaches production |
| **Preconditions** | Customer is on a shade page that offers a tester |
| **Steps** | 1. Stub `POST /store/api/v2/cart` to return HTTP 500.<br>2. Click "Buy a Tester in this colour". |
| **Expected result** | The customer sees "Something has gone wrong, please try again." and never the "successfully added to your cart" confirmation; the basket stays empty |
| **Note** | The error message is a short-lived alert (about 0.7 s to appear, gone after ~3.5 s), so it must be asserted as soon as it appears — see [Lessons Learned #9](LESSONS_LEARNED.md#9-a-short-lived-message-can-hide-from-a-slow-check) |

### TC-06 — Shade with no tester option
| | |
|---|---|
| **Priority** | P3 |
| **Automation** | ✅ [`tester_purchase.feature` — "Desktop customer views a shade that has no tester available"](../features/tester_purchase.feature) (`@negative`) — data-dependent on which shades currently lack a tester |
| **Preconditions** | A shade known to expose only "Find Products in this colour", no "Buy a Tester" button (e.g. "Cotton Breeze" under "Violet" at time of writing — catalogue can drift, see [Lessons Learned #1](LESSONS_LEARNED.md#1-product-catalogue-drift--a-pinned-shade-disappeared-from-its-colour-family)) |
| **Steps** | 1. Start with an empty basket; open the shade's page via the colour finder.<br>2. Confirm "Find Products in this colour" is shown and no "Buy a Tester" control is present.<br>3. Open the basket. |
| **Expected result** | No tester is offered and the basket is still empty. Confirms the assumption behind the pinned-shade decision still holds. As an automated test it also acts as a canary: if it fails, the retailer has added a tester for this shade — pick another shade without one |

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

### TC-09 — Site search returns the searched shade
| | |
|---|---|
| **Priority** | P2 |
| **Automation** | ✅ [`site_navigation.feature` — "Desktop customer searches for a shade"](../features/site_navigation.feature) (outline, 2 examples; `@smoke`) |
| **Preconditions** | On the home page, cookies rejected |
| **Steps** | 1. Open search.<br>2. Enter a term.<br>3. Press Enter. |
| **Expected result** | Known shade ("Romantic Reverie"): the results page `/search-results?search=…` shows that shade. Unknown term ("zzqqxxnoshade"): the results page shows "Sorry, we couldn't find any results for '…'" |

### TC-10 — Cookie banner blocks interaction until dismissed
| | |
|---|---|
| **Priority** | P3 |
| **Automation** | ✅ [`site_navigation.feature` — "Desktop customer cannot use the site until the cookie banner is answered"](../features/site_navigation.feature) |
| **Preconditions** | Fresh browser context, cookie banner not yet interacted with |
| **Steps** | 1. Open the home page.<br>2. Check that the "Find a colour" navigation button cannot be clicked (Playwright trial click, nothing is navigated to).<br>3. Click "Reject all".<br>4. Check the banner is gone and the navigation button can be clicked. |
| **Expected result** | The banner blocks the navigation until "Reject all" is clicked; afterwards it is gone and the page is usable. The banner's buttons are localised (Polish was seen), so the test uses the stable `#onetrust-…` ids, not button text |

### TC-12 — Home page shows the main navigation
| | |
|---|---|
| **Priority** | P2 |
| **Automation** | ✅ [`site_navigation.feature` — "Desktop customer sees the main navigation on the home page"](../features/site_navigation.feature) (`@smoke`) |
| **Preconditions** | On the home page, cookies rejected |
| **Steps** | 1. Look at the top navigation. |
| **Expected result** | The "Find a colour" button, the "Search" button and the "Shopping Cart" link are visible — the entry points of every journey. Only the home page is loaded |

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
