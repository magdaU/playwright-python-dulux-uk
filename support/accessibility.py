from axe_playwright_python.sync_playwright import Axe
from playwright.sync_api import Page

GATED_IMPACTS = {"critical", "serious"}

# Pre-existing production issues on the Dulux site, confirmed while adding
# this scan (2026-08-03) and out of our control (see docs/TEST_STRATEGY.md
# S10). Accepted so the suite doesn't gate on defects we don't own; anything
# NOT in this list at a gated impact level still fails the build.
KNOWN_VIOLATION_IDS = {
    "image-alt",  # shade swatch images missing alt text
    "color-contrast",  # some text/background pairs below WCAG AA contrast
    "label",  # some mobile form controls missing accessible labels
}


def get_unexpected_violations(page: Page) -> list[dict]:
    """Run an axe-core scan and return violations that are both high-impact
    and not already known/accepted — i.e. a genuinely new accessibility
    regression rather than a pre-existing production issue.
    """
    results = Axe().run(page)
    return [
        v
        for v in results.response["violations"]
        if v["impact"] in GATED_IMPACTS and v["id"] not in KNOWN_VIOLATION_IDS
    ]
