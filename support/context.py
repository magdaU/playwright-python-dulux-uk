from playwright.sync_api import Page

from pages.cart_page import CartPage
from pages.color_selection_page import ColorSelectionPage
from pages.components.alert_component import AlertComponent
from pages.components.navigation_component import NavigationComponent
from pages.home_page import HomePage
from support.accessibility import get_unexpected_violations
from support.retry import retry


class Context:
    """Shared browser state + business methods for one scenario.

    Bound to a step_defs test via pytest-bdd's target_fixture on the Given step,
    so later When/Then steps just request the `ctx` fixture — the pytest
    equivalent of the Java project's CucumberContext + PicoContainer DI.
    """

    # Bounded retry for a known-flaky interaction (see browse_to_shade below).
    SHADE_SELECTION_ATTEMPTS = 4

    def __init__(self, page: Page, desktop: bool):
        self.page = page
        self.desktop = desktop
        self.visualizer_tab: Page | None = None

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

    def browse_to_shade(
        self,
        colour_family: str,
        shade: str,
        mobile_navigation: bool,
        tester_available: bool = True,
    ) -> None:
        self.home.open_home_page()

        if mobile_navigation:
            self.navigation.click_dropdown_hamburger_menu()

        self.navigation.click_dropdown_find_colour()
        self.navigation.click_find_colour()

        # Known-flaky on Firefox/WebKit: selecting the colour family
        # occasionally doesn't take effect before the next click queries for
        # a shade button (docs/TEST_STRATEGY.md S10, "Cross-engine navigation
        # timing"). Bounded, explicit retry of just this interaction rather
        # than the whole scenario. A retry reloads the page first — re-issuing
        # the same two clicks on top of a half-applied first attempt was found
        # to leave the shade grid open with no exception raised (the clicks
        # "succeed" but never open the shade detail panel); a fresh reload
        # avoids compounding that state.
        attempted = False

        def select_shade_and_verify() -> None:
            nonlocal attempted
            if attempted:
                self.page.reload()
                self.page.wait_for_load_state()
            attempted = True
            self._select_colour_family_and_shade(colour_family, shade, tester_available)

        retry(
            select_shade_and_verify,
            attempts=self.SHADE_SELECTION_ATTEMPTS,
            description=f'select shade "{shade}" from colour family "{colour_family}"',
        )

    def _select_colour_family_and_shade(self, colour_family: str, shade: str, tester_available: bool) -> None:
        self.color_selection.choose_colour(colour_family)
        self.color_selection.choose_shade(shade)
        # What a successful selection looks like depends on the shade: the tester
        # button, or — for a shade with no tester — only "Find Products in this colour".
        if tester_available:
            self.color_selection.expect_tester_purchase_option_visible()
        else:
            self.color_selection.expect_find_products_option_visible()

    def search_for_shade(self, shade: str) -> None:
        self.navigation.search_click_on_page()
        self.navigation.input_colour_on_search_box_and_enter(shade)

    def add_tester_to_basket(self) -> None:
        self.color_selection.buy_a_tester_colour()
        self.alert.close_alert()

    def fail_add_to_basket_requests(self) -> None:
        # Stubbed in the browser, so the failed request never reaches production.
        def fail(route) -> None:
            if route.request.method == "POST":
                route.fulfill(status=500, content_type="application/json", body='{"error": "stubbed"}')
            else:
                route.continue_()

        self.page.route(self.cart.ADD_TO_BASKET_API_PATTERN, fail)

    def get_unexpected_accessibility_violations(self) -> list[dict]:
        return get_unexpected_violations(self.page)

    def open_visualizer_experience(self) -> None:
        if self.desktop:
            with self.page.context.expect_page() as new_page_info:
                self.color_selection.open_visualizer_app()
            self.visualizer_tab = new_page_info.value
            return

        self.color_selection.open_visualizer_app()
