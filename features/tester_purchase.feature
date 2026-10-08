@purchase @regression
Feature: Purchase a colour tester
  To try a paint colour at home before buying a full tin
  As a Dulux customer
  I want to add a tester for a chosen shade to my basket

  @smoke @desktop
  Scenario: Desktop customer adds a tester from the colour finder
    Given a desktop customer starts with an empty basket
    When the customer browses to shade "Romantic Reverie" from colour family "Violet"
    Then the shade page has no unexpected accessibility violations
    When the customer adds a tester to the basket
    Then the basket contains 1 item
    And the basket includes tester "Dulux Colour Tester" for shade "Romantic Reverie"

  @tablet
  Scenario: Tablet customer adds a tester from the colour finder
    Given a tablet customer starts with an empty basket
    When the customer browses to shade "Romantic Reverie" from colour family "Violet" using tablet navigation
    Then the shade page has no unexpected accessibility violations
    When the customer adds a tester to the basket
    Then the basket contains 1 item
    And the basket includes tester "Dulux Colour Tester" for shade "Romantic Reverie"

  @mobile
  Scenario: Mobile customer adds a tester from the colour finder
    Given a mobile customer starts with an empty basket
    When the customer browses to shade "Romantic Reverie" from colour family "Violet" using mobile navigation
    Then the shade page has no unexpected accessibility violations
    When the customer adds a tester to the basket
    Then the basket contains 1 item
    And the basket includes tester "Dulux Colour Tester" for shade "Romantic Reverie"

  @desktop @boundary
  Scenario Outline: Desktop customer changes the tester quantity at its boundaries
    Given a desktop customer starts with an empty basket
    When the customer browses to shade "Romantic Reverie" from colour family "Violet"
    And the customer adds a tester to the basket
    And the customer changes the tester quantity to <entered>
    Then the basket quantity is <expected>

    # The site accepts 1-23 testers per order. Values outside that range are
    # rejected (HTTP 422) and the field reverts to the last accepted quantity.
    Examples:
      | entered | expected | rule                         |
      | 1       | 1        | minimum accepted             |
      | 23      | 23       | maximum accepted             |
      | 0       | 1        | below minimum, rejected      |
      | 24      | 1        | above maximum, rejected      |
