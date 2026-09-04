# 🔍 Testing Without Business Requirements

> This project tests a real, third-party production site with **no access to a spec,
> ticket, design file, or backlog** — the situation an external tester or developer is
> actually in far more often than a tidy requirements doc would suggest. This document is
> about the skill that implies: what's still meaningfully testable, and how, when the
> "requirements" have to be derived rather than handed to you.

---

## 1. Why this situation is normal, not an edge case

A contractor auditing a client's site, a consultant doing a pre-acquisition technical
review, a new hire testing a legacy system nobody wrote docs for, or — as here — a
portfolio project against a public production site all share the same constraint: no
internal requirements exist to test against. Treating that as a blocker means not testing
at all. Treating it as a design problem produces a different, but still rigorous, kind of
test strategy.

## 2. What replaces a requirements document

| Instead of... | This project uses... |
|---|---|
| A written spec of expected behaviour | The **live UI itself**, read carefully — see the [Features Guide](FEATURES_GUIDE.md), which is a reverse-engineered functional description, not a copy of an internal doc |
| Acceptance criteria from a ticket | **Accessible roles and names** (ARIA semantics) as an implicit contract — a button labelled "Buy a Tester in this colour" states its own intent, testably, without anyone writing it down first |
| A UX spec for "correct" behaviour | **General e-commerce conventions** (empty-basket messaging, quantity controls, confirmation on add-to-cart) as a reasonable, checkable baseline |
| An accessibility requirements doc | **WCAG, via `axe-core`** — an external, objective standard used *in place of* an internal one, so "no new critical/serious violation" is a real, defensible bar even though no one at Dulux wrote it for this project |
| A second team's sign-off on "what should happen" | The **Java sibling project** ([`playwright-java-dulux-uk`](https://github.com/magdaU/playwright-java-dulux-uk)) — an independent second implementation against the same site, useful as a cross-check when something looks like it might be a bug rather than a feature |
| A product owner to ask "is this intended?" | **Explicit non-claims** — behaviour is documented as *observed*, not asserted as *correct*, whenever intent can't actually be confirmed (see §4) |

## 3. Techniques that work without a spec

- **Exploratory testing first, automation second.** Every scenario in this suite started
  as manual exploration of the live site — clicking through the purchase and Visualizer
  flows by hand, across viewports, before writing a single line of Gherkin. Automation
  encodes what exploration already found, it doesn't substitute for it.
- **Cross-configuration comparison as a bug-finding technique.** Running the same
  interaction on desktop vs. mobile, or Chromium vs. Firefox/WebKit, surfaces two
  different kinds of finding: a **deliberate design difference** (mobile Visualizer shows
  a store-data message instead of opening the app — consistent every time, in every run,
  so read as intended behaviour) vs. a **genuine defect or instability** (Firefox/WebKit
  occasionally missing the colour-family selection — inconsistent, engine-specific,
  time-dependent, so read as a real timing bug — see
  [Lessons Learned #3](LESSONS_LEARNED.md#3-cross-engine-navigation-timing--the-same-interaction-behaves-differently-per-browser-engine)).
  The pattern, not a single observation, is what tells them apart.
- **State-based (black-box) verification instead of business-rule verification.** Nobody
  documented that "adding one tester should result in a basket with quantity 1" — but it's
  checkable *as a state transition* (empty → 1 item, correct product, correct shade)
  without needing to know any pricing or inventory rule behind it.
- **Equivalence partitioning from what's observably in the catalogue**, not from a data
  dictionary. A representative shade/family pair stands in for "the colour-finder flow in
  general" — chosen and re-verified by hand, because there's no fixture data to draw from
  instead (see [Lessons Learned #1](LESSONS_LEARNED.md#1-product-catalogue-drift--a-pinned-shade-disappeared-from-its-colour-family)
  for what happens when the chosen instance itself drifts).
- **Accessibility scanning as a requirements substitute, not just a nice-to-have.**
  WCAG/`axe-core` is one of the few *externally defined, objective* bars available when
  there's no internal one — see [Lessons Learned #4](LESSONS_LEARNED.md#4-pre-existing-accessibility-violations-on-a-site-we-dont-own)
  for how that's balanced against not being able to fix violations on a site we don't own.

## 4. What can't be tested this way — and how that's handled honestly

- **Business logic that isn't observable from the UI** (pricing rules, inventory
  thresholds, backend validation) — genuinely untestable black-box, from outside. Not
  claimed as covered anywhere in this project's docs.
- **Whether an observed behaviour is *intended*.** The mobile Visualizer's store-data
  message (see the [Features Guide](FEATURES_GUIDE.md#visualizer-app)) is asserted as
  *what happens*, in the Gherkin's own wording — never phrased as "correctly shows an
  error" or similar, because there's no way to confirm from outside whether it's a bug or
  a deliberate fallback. This distinction — documenting behaviour vs. asserting
  correctness — is the single most important discipline when testing without a
  requirements source, because it's the difference between a test suite that's honest
  about its own limits and one that quietly launders a guess into a "requirement."
- **Whether a fix is *complete*.** A fix can only be verified against what was actually
  observed to be broken (e.g. the `spinbutton` locator narrowed until it uniquely
  matched again — [Lessons Learned #2](LESSONS_LEARNED.md#2-basket-ui-markup-drift--a-redesign-broke-a-locators-uniqueness-not-its-match)),
  not against an intended design the tester was never shown.

## 5. Practical checklist for testing an unfamiliar system with no spec

1. Explore manually first — walk the critical path by hand before writing anything.
2. Write down what you *observe*, separately from what you *assume* is intended.
3. Compare across configurations (viewport, browser, locale) — consistency vs.
   inconsistency is often the only signal available for "is this a feature or a bug".
4. Reach for an external, objective standard (accessibility, security headers, performance
   budgets) wherever one exists — it's requirements you don't have to invent.
5. Verify state transitions, not business rules you can't see.
6. If a second independent implementation or team exists, use disagreement between them as
   a signal worth investigating, not as noise to average away.
7. Say, explicitly, what you couldn't test and why — an honest gap is worth more than a
   test that quietly assumes an answer nobody gave you.

## See also

- [Features Guide](FEATURES_GUIDE.md) — the functional spec this approach produced.
- [Test Strategy §2](TEST_STRATEGY.md#2-system-under-test-sut) — characteristics of the
  system under test that shaped this approach.
- [Lessons Learned](LESSONS_LEARNED.md) — concrete incidents where this way of working
  paid off or had to adapt.
