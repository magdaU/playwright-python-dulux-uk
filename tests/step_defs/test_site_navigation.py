import re
from urllib.parse import quote_plus

import pytest
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import expect
from pytest_bdd import given, parsers, scenarios, then, when

from support.context import Context

scenarios("site_navigation.feature")


@given("a desktop customer is on the home page", target_fixture="ctx")
def desktop_on_home_page(desktop_page):
    ctx = Context(page=desktop_page, desktop=True)
    ctx.open_home_page_and_reject_cookies()
    return ctx


@given("a mobile customer is on the home page", target_fixture="ctx")
def mobile_on_home_page(mobile_page):
    ctx = Context(page=mobile_page, desktop=False)
    ctx.open_home_page_and_reject_cookies()
    return ctx


@given("a tablet customer is on the home page", target_fixture="ctx")
def tablet_on_home_page(tablet_page):
    ctx = Context(page=tablet_page, desktop=False)
    ctx.open_home_page_and_reject_cookies()
    return ctx


@given(
    "a desktop customer opens the home page without answering the cookie banner",
    target_fixture="ctx",
)
def desktop_home_page_banner_unanswered(desktop_page):
    ctx = Context(page=desktop_page, desktop=True)
    ctx.home.open_home_page()
    return ctx


@given(
    "a mobile customer opens the home page without answering the cookie banner",
    target_fixture="ctx",
)
def mobile_home_page_banner_unanswered(mobile_page):
    ctx = Context(page=mobile_page, desktop=False)
    ctx.home.open_home_page()
    return ctx


@when(parsers.parse('the customer searches for "{term}"'))
def search_for_term(ctx, term):
    ctx.search_for_shade(term)


@when("the customer rejects all cookies")
def reject_all_cookies(ctx):
    ctx.home.reject_all_cookies()


@then(parsers.parse('the search results are for "{term}"'))
def search_results_are_for(ctx, term):
    expect(ctx.page).to_have_url(re.compile(rf"/search-results\?search={re.escape(quote_plus(term))}"))


@then(parsers.parse('the results show "{text}"'))
def results_show(ctx, text):
    expect(ctx.page.get_by_text(text).first).to_be_visible()


@then("the cookie banner is shown")
def cookie_banner_is_shown(ctx):
    expect(ctx.home.get_cookie_banner()).to_be_visible()


@then("the cookie banner is gone")
def cookie_banner_is_gone(ctx):
    expect(ctx.home.get_cookie_banner()).to_be_hidden()


@then("the navigation behind the banner cannot be used")
def navigation_blocked_by_banner(ctx):
    # trial=True runs Playwright's actionability checks (including "not covered by another
    # element") without clicking, so nothing is navigated to.
    with pytest.raises(PlaywrightTimeoutError):
        ctx.navigation.get_find_a_colour_button().click(trial=True, timeout=3000)


@then("the navigation can be used")
def navigation_usable(ctx):
    ctx.navigation.get_find_a_colour_button().click(trial=True)


@then("the main navigation offers the colour finder, site search and the shopping cart")
def main_navigation_entry_points(ctx):
    expect(ctx.navigation.get_find_a_colour_button()).to_be_visible()
    expect(ctx.navigation.get_search_button()).to_be_visible()
    expect(ctx.navigation.get_shopping_cart_link()).to_be_visible()


@then("the responsive navigation offers the menu, site search and the shopping cart")
def responsive_navigation_entry_points(ctx):
    expect(ctx.navigation.get_menu_button()).to_be_visible()
    expect(ctx.navigation.get_search_button()).to_be_visible()
    expect(ctx.navigation.get_shopping_cart_link()).to_be_visible()
