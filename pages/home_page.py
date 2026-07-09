from pages.base_page import BasePage


class HomePage(BasePage):
    URL = "https://www.dulux.co.uk"
    REJECT_ALL = "#onetrust-reject-all-handler"

    def open_home_page(self) -> None:
        self.page.goto(self.URL)
        self.page.wait_for_load_state()

    def reject_all_cookies(self) -> None:
        self.page.locator(self.REJECT_ALL).click()
