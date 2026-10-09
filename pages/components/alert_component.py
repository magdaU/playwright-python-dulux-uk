from playwright.sync_api import Locator

from pages.base_page import BasePage


class AlertComponent(BasePage):
    def get_alert(self) -> Locator:
        return self.page.get_by_role("alert")

    def close_alert(self) -> None:
        self.page.get_by_role("alert").get_by_role("button").click()
