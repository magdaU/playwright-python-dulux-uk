from playwright.sync_api import Locator, Response

from pages.base_page import BasePage


class CartPage(BasePage):
    CART_PAGE_URL = "https://www.dulux.co.uk/en/store/cart"
    ORDER_API_PATH = "/store/api/order"
    QUANTITY_INPUT_LABEL = "Quantity input"
    INCREASE_QUANTITY_LABEL = "Increase quantity"
    DECREASE_QUANTITY_LABEL = "Decrease quantity"
    REMOVE_ITEM_LABEL = "Remove"
    ADD_TO_BASKET_API_PATTERN = "**/store/api/v2/cart"
    ADD_TO_BASKET_URL = "https://www.dulux.co.uk/en/store/api/v2/cart"
    YOUR_BASKET_IS_EMPTY_TEXT = "Your basket is empty"

    def open_cart_page(self) -> None:
        self.page.goto(self.CART_PAGE_URL)

    def reload(self) -> None:
        self.page.reload()

    def find_amount(self, amount: str) -> Locator:
        return self.page.get_by_text(amount, exact=True)

    def get_quantity(self) -> Locator:
        return self.page.get_by_role("spinbutton", name=self.QUANTITY_INPUT_LABEL)

    def change_quantity(self, quantity: int) -> None:
        field = self.get_quantity()
        # The field's own min/max are enforced client-side: values outside them
        # (or unchanged) never reach the server. Anything else is validated
        # server-side, which can still reject it (HTTP 422) and revert the field —
        # so wait for that verdict instead of reading the field's transient value.
        reaches_server = int(field.get_attribute("min")) <= quantity <= int(
            field.get_attribute("max")
        ) and field.input_value() != str(quantity)
        if reaches_server:
            with self.page.expect_response(self._is_order_update):
                self._commit_quantity(field, quantity)
        else:
            self._commit_quantity(field, quantity)

    @staticmethod
    def _commit_quantity(field: Locator, quantity: int) -> None:
        field.fill(str(quantity))
        field.press("Tab")  # blur commits the change

    @classmethod
    def _is_order_update(cls, response: Response) -> bool:
        return response.request.method == "POST" and response.url.endswith(cls.ORDER_API_PATH)

    def get_increase_button(self) -> Locator:
        return self.page.get_by_role("button", name=self.INCREASE_QUANTITY_LABEL)

    def get_decrease_button(self) -> Locator:
        return self.page.get_by_role("button", name=self.DECREASE_QUANTITY_LABEL)

    def get_remove_button(self) -> Locator:
        return self.page.get_by_role("button", name=self.REMOVE_ITEM_LABEL)

    def increase_quantity(self) -> None:
        self.get_increase_button().click()

    def decrease_quantity(self) -> None:
        self.get_decrease_button().click()

    def remove_item(self) -> None:
        self.get_remove_button().click()

    def find_text(self, text: str) -> Locator:
        return self.page.get_by_text(text)

    def get_basket_empty_text(self) -> Locator:
        return self.page.get_by_text(self.YOUR_BASKET_IS_EMPTY_TEXT)
