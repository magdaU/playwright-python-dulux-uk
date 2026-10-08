@purchase @regression
Feature: Purchase a colour tester
  To try a paint colour at home before buying a full tin
  As a Dulux customer
  I want to add a tester for a chosen shade to my basket

  @smoke @desktop
  Scenario: Desktop customer adds a tester from the colour finder
    The critical purchase path (TC-01). The customer finds a shade through the colour finder
    in the top navigation, adds a tester to the basket and must end up with exactly one tester
    for that shade. The shade page is also scanned for new serious or critical accessibility
    violations.
    Given a desktop customer starts with an empty basket
    When the customer browses to shade "Romantic Reverie" from colour family "Violet"
    Then the shade page has no unexpected accessibility violations
    When the customer adds a tester to the basket
    Then the basket contains 1 item
    And the basket includes tester "Dulux Colour Tester" for shade "Romantic Reverie"

  @tablet
  Scenario: Tablet customer adds a tester from the colour finder
    The same purchase path on a tablet (TC-02). At this width the site collapses to the
    hamburger-menu navigation, so the colour finder is reached through the menu.
    Given a tablet customer starts with an empty basket
    When the customer browses to shade "Romantic Reverie" from colour family "Violet" using tablet navigation
    Then the shade page has no unexpected accessibility violations
    When the customer adds a tester to the basket
    Then the basket contains 1 item
    And the basket includes tester "Dulux Colour Tester" for shade "Romantic Reverie"

  @mobile
  Scenario: Mobile customer adds a tester from the colour finder
    The same purchase path on a phone (TC-03), reached through the hamburger menu.
    Given a mobile customer starts with an empty basket
    When the customer browses to shade "Romantic Reverie" from colour family "Violet" using mobile navigation
    Then the shade page has no unexpected accessibility violations
    When the customer adds a tester to the basket
    Then the basket contains 1 item
    And the basket includes tester "Dulux Colour Tester" for shade "Romantic Reverie"

  @desktop @boundary
  Scenario Outline: Desktop customer changes the tester quantity at its boundaries
    Boundary values for the basket quantity (TC-04a). The field declares a maximum of 999, but
    the server only accepts 1 to 23 testers: a value outside that range is rejected (HTTP 422)
    and the field settles back on the last accepted quantity.
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
