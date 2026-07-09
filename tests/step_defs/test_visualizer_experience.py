from playwright.sync_api import expect
from pytest_bdd import given, parsers, scenarios, then, when

from support.context import Context

scenarios("visualizer_experience.feature")


@given(parsers.parse('a desktop customer is viewing shade "{shade}"'), target_fixture="ctx")
def desktop_viewing_shade(desktop_page, shade):
    ctx = Context(page=desktop_page, desktop=True)
    ctx.open_home_page_and_reject_cookies()
    ctx.search_for_shade(shade)
    return ctx


@given(parsers.parse('a mobile customer is viewing shade "{shade}"'), target_fixture="ctx")
def mobile_viewing_shade(mobile_page, shade):
    ctx = Context(page=mobile_page, desktop=False)
    ctx.open_home_page_and_reject_cookies()
    ctx.search_for_shade(shade)
    return ctx


@when("the customer opens the Visualizer experience")
def open_visualizer(ctx):
    ctx.open_visualizer_experience()


@then("the Visualizer opens in a new tab")
def visualizer_opens_new_tab(ctx):
    assert ctx.desktop
    assert ctx.visualizer_tab is not None


@then(parsers.parse('the Visualizer page URL is "{url}"'))
def visualizer_page_url(ctx, url):
    assert ctx.visualizer_tab.url == url


@then(parsers.parse('the page shows message "{message}"'))
def page_shows_message(ctx, message):
    pre = ctx.page.locator("pre")
    expect(pre).to_be_visible()
    assert message in pre.text_content()
