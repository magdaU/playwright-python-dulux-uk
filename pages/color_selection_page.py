from playwright.sync_api import Locator

from pages.base_page import BasePage


class ColorSelectionPage(BasePage):
    BUY_A_TESTER_TEXT = "Buy a Tester in this colour"
    FIND_PRODUCTS_TEXT = "Find Products in this colour"
    VISUALIZER_APP_TEXT = "Try our Visualizer App"

    def choose_colour(self, colour_family: str) -> None:
        self._click_button_by_name(colour_family)

    def choose_shade(self, shade: str) -> None:
        self._click_button_by_name(shade)

    def buy_a_tester_colour(self) -> None:
        self.page.get_by_role("button", name=self.BUY_A_TESTER_TEXT).click()

    def expect_tester_purchase_option_visible(self) -> None:
        # Confirms the shade detail panel actually opened, not just that the
        # shade button's click event fired (see docs/TEST_STRATEGY.md S10,
        # "Cross-engine navigation timing" — on Firefox/WebKit the click can
        # silently no-op if it lands before the just-rendered grid finishes
        # hydrating, leaving the grid view showing with no exception raised).
        self.page.get_by_role("button", name=self.BUY_A_TESTER_TEXT).wait_for(state="visible", timeout=8000)

    def expect_find_products_option_visible(self) -> None:
        # The no-tester counterpart of expect_tester_purchase_option_visible: for a
        # shade without a tester the detail panel offers only "Find Products in this
        # colour", so this confirms the panel opened rather than the click no-opping.
        self.get_find_products_text().wait_for(state="visible", timeout=8000)

    def get_find_products_text(self) -> Locator:
        return self.page.get_by_text(self.FIND_PRODUCTS_TEXT)

    def get_buy_a_tester_button(self) -> Locator:
        return self.page.get_by_role("button", name=self.BUY_A_TESTER_TEXT)

    def open_visualizer_app(self) -> None:
        self.page.get_by_role("listitem").filter(has_text=self.VISUALIZER_APP_TEXT).get_by_role(
            "link"
        ).click()

    def _click_button_by_name(self, name: str) -> None:
        self.page.get_by_role("button", name=name).click()
