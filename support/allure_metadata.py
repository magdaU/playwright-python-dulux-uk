"""Allure report metadata (epic, story, severity, owner, test-case link) per scenario.

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

BUYING = "Buying paint"
EXPLORING = "Exploring colours"


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


def apply_allure_metadata(item: pytest.Item, scenario_name: str, test_cases: dict) -> None:
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
            apply_allure_metadata(item, scenario.name, test_cases)
