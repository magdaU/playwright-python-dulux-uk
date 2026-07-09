from pages.base_page import BasePage


class AlertComponent(BasePage):
    def close_alert(self) -> None:
        self.page.get_by_role("alert").get_by_role("button").click()
