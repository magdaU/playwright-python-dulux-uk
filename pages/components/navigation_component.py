from pages.base_page import BasePage


class NavigationComponent(BasePage):
    FIND_A_COLOUR_MENU_ITEM = "Find a colour"
    MENU_HAMBURGER = "Menu"
    SHOPPING_CART = "Shopping Cart"
    SEARCH_FIELD = "search-field"
    SEARCH_BUTTON = "Search"

    def click_dropdown_find_colour(self) -> None:
        self.page.get_by_role("button", name=self.FIND_A_COLOUR_MENU_ITEM).click()
        # The button triggers a page navigation (not a dropdown). Wait for the new
        # page to load before proceeding — without this, the next click resolves
        # against the outgoing page and hits a stale element.
        self.page.wait_for_load_state()

    def click_dropdown_hamburger_menu(self) -> None:
        self.page.get_by_role("button", name=self.MENU_HAMBURGER).click()

    def click_find_colour(self) -> None:
        self.page.get_by_role("link", name=self.FIND_A_COLOUR_MENU_ITEM).click()

    def open_shopping_cart(self) -> None:
        self.page.get_by_role("link", name=self.SHOPPING_CART).click()

    def search_click_on_page(self) -> None:
        self.page.get_by_role("button", name=self.SEARCH_BUTTON).click()

    def input_colour_on_search_box_and_enter(self, colour: str) -> None:
        search_field = self.page.get_by_role("textbox", name=self.SEARCH_FIELD)
        search_field.fill(colour)
        search_field.press("Enter")
