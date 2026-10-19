from playwright.sync_api import Locator

from pages.base_page import BasePage


class HomePage(BasePage):
    URL = "https://www.dulux.co.uk"
    REJECT_ALL = "#onetrust-reject-all-handler"
    COOKIE_BANNER = "#onetrust-banner-sdk"

    def open_home_page(self) -> None:
        # "load" waits for every sub-resource and timed out on the slow CI runner while the
        # page was already usable; each later step waits for its own element.
        self.page.goto(self.URL, wait_until="domcontentloaded")

    def get_cookie_banner(self) -> Locator:
        return self.page.locator(self.COOKIE_BANNER)

    def reject_all_cookies(self) -> None:
        self.page.locator(self.REJECT_ALL).click()
