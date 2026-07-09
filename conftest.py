import pytest
from playwright.sync_api import Browser, Page

DESKTOP_VIEWPORT = {"width": 1920, "height": 1080}
MOBILE_VIEWPORT = {"width": 375, "height": 667}


def _page_with_viewport(browser: Browser, viewport: dict) -> Page:
    context = browser.new_context(viewport=viewport)
    page = context.new_page()
    yield page
    context.close()


@pytest.fixture
def desktop_page(browser: Browser) -> Page:
    yield from _page_with_viewport(browser, DESKTOP_VIEWPORT)


@pytest.fixture
def mobile_page(browser: Browser) -> Page:
    yield from _page_with_viewport(browser, MOBILE_VIEWPORT)
