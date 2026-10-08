from playwright.sync_api import expect
from pytest_bdd import given, parsers, scenarios, then, when

from support.context import Context

scenarios("tester_purchase.feature")

FAILED_ADD_MESSAGE = "Something has gone wrong, please try again."
SUCCESS_MESSAGE = "successfully added to your cart"


@given("a desktop customer starts with an empty basket", target_fixture="ctx")
def desktop_empty_basket(desktop_page):
    ctx = Context(page=desktop_page, desktop=True)
    ctx.open_empty_cart()
    expect(ctx.cart.get_basket_empty_text()).to_be_visible()
    return ctx


@given("a tablet customer starts with an empty basket", target_fixture="ctx")
def tablet_empty_basket(tablet_page):
    ctx = Context(page=tablet_page, desktop=False)
    ctx.open_empty_cart()
    expect(ctx.cart.get_basket_empty_text()).to_be_visible()
    return ctx


@given("a mobile customer starts with an empty basket", target_fixture="ctx")
def mobile_empty_basket(mobile_page):
    ctx = Context(page=mobile_page, desktop=False)
    ctx.open_empty_cart()
    expect(ctx.cart.get_basket_empty_text()).to_be_visible()
    return ctx


@when(parsers.parse('the customer browses to shade "{shade}" from colour family "{colour_family}"'))
def browse_to_shade(ctx, shade, colour_family):
    ctx.browse_to_shade(colour_family, shade, mobile_navigation=False)


@when(
    parsers.re(
        r'the customer browses to shade "(?P<shade>[^"]+)" from colour family "(?P<colour_family>[^"]+)"'
        r" using (?:tablet|mobile) navigation"
    )
)
def browse_to_shade_hamburger_menu(ctx, shade, colour_family):
    # Tablet portrait collapses to the same hamburger-menu navigation as
    # mobile (confirmed against production — see docs/TEST_STRATEGY.md S13,
    # "Tablet viewport"), so one step definition covers both phrasings.
    ctx.browse_to_shade(colour_family, shade, mobile_navigation=True)


@when(parsers.parse('the customer opens shade "{shade}" from colour family "{colour_family}"'))
def open_shade_without_tester(ctx, shade, colour_family):
    ctx.browse_to_shade(colour_family, shade, mobile_navigation=False, tester_available=False)


@when("the customer increases the tester quantity")
def increase_tester_quantity(ctx):
    ctx.cart.increase_quantity()


@when("the customer decreases the tester quantity")
def decrease_tester_quantity(ctx):
    ctx.cart.decrease_quantity()


@when("the customer removes the tester from the basket")
def remove_tester_from_basket(ctx):
    ctx.cart.remove_item()


@when("the add-to-basket request fails")
def add_to_basket_request_fails(ctx):
    ctx.fail_add_to_basket_requests()


@when("the customer tries to add a tester to the basket")
def try_to_add_tester(ctx):
    ctx.color_selection.buy_a_tester_colour()


@when("the customer adds a tester to the basket")
def add_tester_to_basket(ctx):
    ctx.add_tester_to_basket()
    ctx.navigation.open_shopping_cart()


@when(parsers.parse("the customer changes the tester quantity to {quantity:d}"))
def change_tester_quantity(ctx, quantity):
    ctx.cart.change_quantity(quantity)


@then(parsers.parse("the basket quantity is {quantity:d}"))
def basket_quantity_is(ctx, quantity):
    # Auto-waits, so a rejected value (which reverts after the server's 422)
    # is only accepted once the field has settled on the expected quantity.
    expect(ctx.cart.get_quantity()).to_have_value(str(quantity))


@then("the tester quantity cannot be decreased any further")
def quantity_is_at_minimum(ctx):
    expect(ctx.cart.get_decrease_button()).to_be_disabled()


@then("the basket is empty")
def basket_is_empty(ctx):
    expect(ctx.cart.get_basket_empty_text()).to_be_visible()


@then("the customer is told something went wrong")
def customer_told_something_went_wrong(ctx):
    expect(ctx.alert.get_alert()).to_contain_text(FAILED_ADD_MESSAGE)


@then("the customer is not told the tester was added")
def customer_not_told_tester_added(ctx):
    messages = ctx.alert.get_alert().all_inner_texts()
    assert not any(SUCCESS_MESSAGE in message for message in messages), messages


@then("the shade offers products but no tester to buy")
def shade_offers_no_tester(ctx):
    expect(ctx.color_selection.get_find_products_text()).to_be_visible()
    expect(ctx.color_selection.get_buy_a_tester_button()).to_have_count(0)


@then("the basket is still empty")
def basket_is_still_empty(ctx):
    ctx.navigation.open_shopping_cart()
    expect(ctx.cart.get_basket_empty_text()).to_be_visible()


@then(parsers.parse("the basket contains {count:d} item"))
def basket_contains_items(ctx, count):
    expect(ctx.cart.get_quantity()).to_have_value(str(count))


@then(parsers.parse('the basket includes tester "{tester_name}" for shade "{shade}"'))
def basket_includes_tester(ctx, tester_name, shade):
    expect(ctx.cart.find_text(tester_name)).to_be_visible()
    expect(ctx.cart.find_text(shade)).to_be_visible()


@then("the shade page has no unexpected accessibility violations")
def shade_page_has_no_unexpected_a11y_violations(ctx):
    violations = ctx.get_unexpected_accessibility_violations()
    assert not violations, [f"{v['impact']}:{v['id']}" for v in violations]
