from playwright.sync_api import Locator

from pages.base_page import BasePage


class CartPage(BasePage):
    CART_PAGE_URL = "https://www.dulux.co.uk/en/store/cart"
    QUANTITY_INPUT_LABEL = "Quantity input"
    YOUR_BASKET_IS_EMPTY_TEXT = "Your basket is empty"

    def open_cart_page(self) -> None:
        self.page.goto(self.CART_PAGE_URL)

    def get_quantity(self) -> Locator:
        return self.page.get_by_role("spinbutton", name=self.QUANTITY_INPUT_LABEL)

    def find_text(self, text: str) -> Locator:
        return self.page.get_by_text(text)

    def get_basket_empty_text(self) -> Locator:
        return self.page.get_by_text(self.YOUR_BASKET_IS_EMPTY_TEXT)
