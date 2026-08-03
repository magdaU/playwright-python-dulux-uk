from typing import Optional

from playwright.sync_api import Page

from pages.cart_page import CartPage
from pages.color_selection_page import ColorSelectionPage
from pages.components.alert_component import AlertComponent
from pages.components.navigation_component import NavigationComponent
from pages.home_page import HomePage
from support.accessibility import get_unexpected_violations


class Context:
    """Shared browser state + business methods for one scenario.

    Bound to a step_defs test via pytest-bdd's target_fixture on the Given step,
    so later When/Then steps just request the `ctx` fixture — the pytest
    equivalent of the Java project's CucumberContext + PicoContainer DI.
    """

    def __init__(self, page: Page, desktop: bool):
        self.page = page
        self.desktop = desktop
        self.visualizer_tab: Optional[Page] = None

        self.home = HomePage(page)
        self.navigation = NavigationComponent(page)
        self.color_selection = ColorSelectionPage(page)
        self.cart = CartPage(page)
        self.alert = AlertComponent(page)

    def open_empty_cart(self) -> None:
        self.cart.open_cart_page()
        self.home.reject_all_cookies()

    def open_home_page_and_reject_cookies(self) -> None:
        self.home.open_home_page()
        self.home.reject_all_cookies()

    def browse_to_shade(self, colour_family: str, shade: str, mobile_navigation: bool) -> None:
        self.home.open_home_page()

        if mobile_navigation:
            self.navigation.click_dropdown_hamburger_menu()

        self.navigation.click_dropdown_find_colour()
        self.navigation.click_find_colour()
        self.color_selection.choose_colour(colour_family)
        self.color_selection.choose_shade(shade)

    def search_for_shade(self, shade: str) -> None:
        self.navigation.search_click_on_page()
        self.navigation.input_colour_on_search_box_and_enter(shade)

    def add_tester_to_basket(self) -> None:
        self.color_selection.buy_a_tester_colour()
        self.alert.close_alert()

    def get_unexpected_accessibility_violations(self) -> list[dict]:
        return get_unexpected_violations(self.page)

    def open_visualizer_experience(self) -> None:
        if self.desktop:
            with self.page.context.expect_page() as new_page_info:
                self.color_selection.open_visualizer_app()
            self.visualizer_tab = new_page_info.value
            return

        self.color_selection.open_visualizer_app()
