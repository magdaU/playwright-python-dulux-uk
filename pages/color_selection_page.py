from pages.base_page import BasePage


class ColorSelectionPage(BasePage):
    BUY_A_TESTER_TEXT = "Buy a Tester in this colour"
    VISUALIZER_APP_TEXT = "Try our Visualizer App"

    def choose_colour(self, colour_family: str) -> None:
        self._click_button_by_name(colour_family)

    def choose_shade(self, shade: str) -> None:
        self._click_button_by_name(shade)

    def buy_a_tester_colour(self) -> None:
        self.page.get_by_role("button", name=self.BUY_A_TESTER_TEXT).click()

    def open_visualizer_app(self) -> None:
        self.page.get_by_role("listitem").filter(
            has_text=self.VISUALIZER_APP_TEXT
        ).get_by_role("link").click()

    def _click_button_by_name(self, name: str) -> None:
        self.page.get_by_role("button", name=name).click()
