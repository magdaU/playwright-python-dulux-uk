from pytest_bdd import scenarios, given, when, then, parsers

scenarios("tester_purchase.feature")

# TODO: port TesterProductTest.java + CucumberContext.java business steps.
# Given/When/Then bodies below are placeholders wiring page objects together.


@given("a desktop customer starts with an empty basket")
def desktop_empty_basket(desktop_page):
    raise NotImplementedError


@given("a mobile customer starts with an empty basket")
def mobile_empty_basket(mobile_page):
    raise NotImplementedError


@when(parsers.parse('the customer browses to shade "{shade}" from colour family "{colour_family}"'))
def browse_to_shade(shade, colour_family):
    raise NotImplementedError


@when(parsers.parse(
    'the customer browses to shade "{shade}" from colour family "{colour_family}" using mobile navigation'
))
def browse_to_shade_mobile(shade, colour_family):
    raise NotImplementedError


@when("the customer adds a tester to the basket")
def add_tester_to_basket():
    raise NotImplementedError


@then(parsers.parse("the basket contains {count:d} item"))
def basket_contains_items(count):
    raise NotImplementedError


@then(parsers.parse('the basket includes tester "{tester_name}" for shade "{shade}"'))
def basket_includes_tester(tester_name, shade):
    raise NotImplementedError
