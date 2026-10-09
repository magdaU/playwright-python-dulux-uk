"""Allure report metadata (epic, story, severity, owner, test-case link, viewport suite) per scenario.

The scenario -> test case (TC-xx) mapping lives here; everything else about a test
case — its priority and the anchor of its write-up — is read from docs/TEST_CASES.md,
so the docs stay the single source of truth and a report link can never point at a
heading that no longer exists (a missing TC fails collection loudly instead).
"""

import re
from dataclasses import dataclass
from pathlib import Path

import pytest

TEST_CASES_DOC = Path(__file__).resolve().parent.parent / "docs" / "TEST_CASES.md"
TEST_CASES_URL = "https://github.com/magdaU/playwright-python-dulux-uk/blob/main/docs/TEST_CASES.md"
OWNER = "magdaU"

SEVERITY_BY_PRIORITY = {"P1": "critical", "P2": "normal", "P3": "minor"}

# The @desktop/@tablet/@mobile tag a scenario already carries decides its top-level
# group in the report's Suites tab, so the viewport is never declared twice.
VIEWPORT_SUITES = {"desktop": "Desktop", "tablet": "Tablet", "mobile": "Mobile"}

BUYING = "Buying paint"
EXPLORING = "Exploring colours"
USING_THE_SITE = "Using the site"


@dataclass(frozen=True)
class ScenarioMetadata:
    test_case: str
    epic: str
    story: str


SCENARIOS = {
    "Desktop customer adds a tester from the colour finder": ScenarioMetadata(
        "TC-01", BUYING, "Add a tester to the basket"
    ),
    "Tablet customer adds a tester from the colour finder": ScenarioMetadata(
        "TC-02", BUYING, "Add a tester to the basket"
    ),
    "Mobile customer adds a tester from the colour finder": ScenarioMetadata(
        "TC-03", BUYING, "Add a tester to the basket"
    ),
    "Desktop customer changes the basket quantity and removes the tester": ScenarioMetadata(
        "TC-04", BUYING, "Edit the basket"
    ),
    "Desktop customer is told when adding a tester to the basket fails": ScenarioMetadata(
        "TC-05", BUYING, "Handle a failed add to the basket"
    ),
    "Desktop customer searches for a shade": ScenarioMetadata("TC-09", EXPLORING, "Search for a shade"),
    "Desktop customer cannot use the site until the cookie banner is answered": ScenarioMetadata(
        "TC-10", USING_THE_SITE, "Cookie consent"
    ),
    "Desktop customer sees the main navigation on the home page": ScenarioMetadata(
        "TC-12", USING_THE_SITE, "Main navigation"
    ),
    "Desktop customer adds a tester for a shade from another colour family": ScenarioMetadata(
        "TC-13", BUYING, "Add a tester to the basket"
    ),
    "Desktop customer sees the price of a tester and the order total": ScenarioMetadata(
        "TC-14", BUYING, "See the price"
    ),
    "Desktop customer finds the basket unchanged after reloading the page": ScenarioMetadata(
        "TC-15", BUYING, "Edit the basket"
    ),
    "Desktop customer can open a shade from the colour finder": ScenarioMetadata(
        "TC-16", BUYING, "Find a shade"
    ),
    "Desktop customer with nothing in the basket is told so and can keep shopping": ScenarioMetadata(
        "TC-17", BUYING, "Leave the basket"
    ),
    "Desktop customer can leave the basket and keep shopping": ScenarioMetadata(
        "TC-18", BUYING, "Leave the basket"
    ),
    "Mobile customer answers the cookie banner": ScenarioMetadata("TC-19", USING_THE_SITE, "Cookie consent"),
    "Mobile customer sees the menu on the home page": ScenarioMetadata(
        "TC-20", USING_THE_SITE, "Main navigation"
    ),
    "Tablet customer sees the menu on the home page": ScenarioMetadata(
        "TC-21", USING_THE_SITE, "Main navigation"
    ),
    "Desktop customer views a shade that has no tester available": ScenarioMetadata(
        "TC-06", BUYING, "Shade without a tester option"
    ),
    "Desktop customer changes the tester quantity at its boundaries": ScenarioMetadata(
        "TC-04a", BUYING, "Change the tester quantity"
    ),
    "Desktop customer opens the Visualizer for a shade": ScenarioMetadata(
        "TC-07", EXPLORING, "Open the Visualizer"
    ),
    "Mobile customer tries to open the Visualizer for a shade": ScenarioMetadata(
        "TC-08", EXPLORING, "Open the Visualizer"
    ),
}

_TEST_CASE_HEADING = re.compile(r"^### (TC-\w+) — (.+)$", re.MULTILINE)
_PRIORITY = re.compile(r"\*\*Priority\*\* \| (P\d)")


def _anchor(heading: str) -> str:
    # GitHub's heading slug: lower-case, punctuation dropped, spaces -> hyphens.
    slug = re.sub(r"[^\w\s-]", "", heading.lower())
    return slug.replace(" ", "-")


def _read_test_cases() -> dict[str, tuple[str, str]]:
    """TC id -> (priority, anchor), parsed from docs/TEST_CASES.md."""
    text = TEST_CASES_DOC.read_text(encoding="utf-8")
    headings = list(_TEST_CASE_HEADING.finditer(text))
    test_cases = {}
    for heading, following in zip(headings, [*headings[1:], None], strict=True):
        section = text[heading.end() : following.start() if following else len(text)]
        priority = _PRIORITY.search(section)
        test_cases[heading.group(1)] = (
            priority.group(1) if priority else "",
            _anchor(heading.group(0).removeprefix("### ")),
        )
    return test_cases


def apply_allure_metadata(item: pytest.Item, scenario, test_cases: dict) -> None:
    scenario_name = scenario.name
    metadata = SCENARIOS.get(scenario_name)
    if metadata is None:
        return

    if metadata.test_case not in test_cases:
        raise pytest.UsageError(
            f'{metadata.test_case} (scenario "{scenario_name}") not found in {TEST_CASES_DOC.name}'
        )
    priority, anchor = test_cases[metadata.test_case]
    if priority not in SEVERITY_BY_PRIORITY:
        raise pytest.UsageError(f"{metadata.test_case} has no recognised Priority in {TEST_CASES_DOC.name}")

    labels = {
        "epic": metadata.epic,
        "story": metadata.story,
        "owner": OWNER,
        "severity": SEVERITY_BY_PRIORITY[priority],
    }
    viewport = next((name for name in VIEWPORT_SUITES if item.get_closest_marker(name)), None)
    if viewport:
        labels["parentSuite"] = VIEWPORT_SUITES[viewport]
        labels["suite"] = scenario.feature.name  # keeps the feature level under the viewport group
    for label_type, value in labels.items():
        item.add_marker(pytest.mark.allure_label(value, label_type=label_type))
    item.add_marker(
        pytest.mark.allure_link(f"{TEST_CASES_URL}#{anchor}", name=metadata.test_case, link_type="tms")
    )


def apply_to_items(items: list[pytest.Item]) -> None:
    test_cases = _read_test_cases()
    for item in items:
        scenario = getattr(getattr(item, "obj", None), "__scenario__", None)
        if scenario is not None:
            apply_allure_metadata(item, scenario, test_cases)
