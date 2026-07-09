from pytest_bdd import scenarios, given, when, then, parsers

scenarios("visualizer_experience.feature")

# TODO: port VisualizerAppTest.java + CucumberContext.java business steps.


@given(parsers.parse('a desktop customer is viewing shade "{shade}"'))
def desktop_viewing_shade(desktop_page, shade):
    raise NotImplementedError


@given(parsers.parse('a mobile customer is viewing shade "{shade}"'))
def mobile_viewing_shade(mobile_page, shade):
    raise NotImplementedError


@when("the customer opens the Visualizer experience")
def open_visualizer():
    raise NotImplementedError


@then("the Visualizer opens in a new tab")
def visualizer_opens_new_tab():
    raise NotImplementedError


@then(parsers.parse('the Visualizer page URL is "{url}"'))
def visualizer_page_url(url):
    raise NotImplementedError


@then(parsers.parse('the page shows message "{message}"'))
def page_shows_message(message):
    raise NotImplementedError
