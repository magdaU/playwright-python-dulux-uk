from playwright.sync_api import expect
from pytest_bdd import given, parsers, scenarios, then, when

from support.context import Context

scenarios("tester_purchase.feature")


@given("a desktop customer starts with an empty basket", target_fixture="ctx")
def desktop_empty_basket(desktop_page):
    ctx = Context(page=desktop_page, desktop=True)
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


@when(parsers.parse(
    'the customer browses to shade "{shade}" from colour family "{colour_family}" using mobile navigation'
))
def browse_to_shade_mobile(ctx, shade, colour_family):
    ctx.browse_to_shade(colour_family, shade, mobile_navigation=True)


@when("the customer adds a tester to the basket")
def add_tester_to_basket(ctx):
    ctx.add_tester_to_basket()
    ctx.navigation.open_shopping_cart()


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
