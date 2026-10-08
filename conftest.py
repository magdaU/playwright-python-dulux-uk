import pytest
from playwright.sync_api import Browser, Page

import allure
from support.allure_metadata import apply_to_items

DESKTOP_VIEWPORT = {"width": 1920, "height": 1080}
TABLET_VIEWPORT = {"width": 768, "height": 1024}
MOBILE_VIEWPORT = {"width": 375, "height": 667}


def pytest_collection_modifyitems(items):
    apply_to_items(items)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Expose each phase's outcome on the test item (item.rep_setup / rep_call),
    # so a fixture can tell at teardown whether the test failed.
    outcome = yield
    setattr(item, f"rep_{call.when}", outcome.get_result())


def _attach_failure_evidence(page: Page) -> None:
    # Allure shows these on the failed test, so a red run is diagnosable without
    # re-running it against production (where the page may already have changed).
    allure.attach(page.url, name="page-url", attachment_type=allure.attachment_type.TEXT)
    allure.attach(
        page.screenshot(full_page=True),
        name="screenshot-on-failure",
        attachment_type=allure.attachment_type.PNG,
    )


def _test_failed(item) -> bool:
    reports = (getattr(item, f"rep_{phase}", None) for phase in ("setup", "call"))
    return any(report and report.failed for report in reports)


def _page_with_viewport(browser: Browser, viewport: dict, item) -> Page:
    context = browser.new_context(viewport=viewport)
    page = context.new_page()
    yield page
    if _test_failed(item):
        _attach_failure_evidence(page)
    context.close()


@pytest.fixture
def desktop_page(browser: Browser, request) -> Page:
    yield from _page_with_viewport(browser, DESKTOP_VIEWPORT, request.node)


@pytest.fixture
def tablet_page(browser: Browser, request) -> Page:
    yield from _page_with_viewport(browser, TABLET_VIEWPORT, request.node)


@pytest.fixture
def mobile_page(browser: Browser, request) -> Page:
    yield from _page_with_viewport(browser, MOBILE_VIEWPORT, request.node)
