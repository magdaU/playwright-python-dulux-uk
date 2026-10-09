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

  @desktop @negative
  Scenario: Desktop customer views a shade that has no tester available
    Negative path (TC-06). Not every shade can be bought as a tester: "Cotton Breeze" offers
    only "Find Products in this colour". The customer must not be offered a tester to buy,
    and the basket must stay empty. If the retailer ever adds a tester for this shade the test
    fails, flagging catalogue drift in the pinned-shade assumption.
    Given a desktop customer starts with an empty basket
    When the customer opens shade "Cotton Breeze" from colour family "Violet"
    Then the shade offers products but no tester to buy
    And the basket is still empty

  @desktop @boundary
  Scenario Outline: Desktop customer changes the tester quantity at its boundaries
    Boundary values for the basket quantity (TC-04a). The field declares a maximum of 999, but
    the server only accepts 1 to 23 testers: a value outside that range is rejected (HTTP 422)
    and the field settles back on the last accepted quantity. The basket is seeded through the
    site's own add-to-cart API, so each example loads only the basket page.
    Given a desktop customer has a tester for shade "Romantic Reverie" in the basket
    When the customer changes the tester quantity to <entered>
    Then the basket quantity is <expected>

    # The site accepts 1-23 testers per order. Values outside that range are
    # rejected (HTTP 422) and the field reverts to the last accepted quantity.
    Examples:
      | entered | expected | rule                         |
      | 1       | 1        | minimum accepted             |
      | 23      | 23       | maximum accepted             |
      | 0       | 1        | below minimum, rejected      |
      | 24      | 1        | above maximum, rejected      |

  @desktop
  Scenario: Desktop customer changes the basket quantity and removes the tester
    Editing the basket after a purchase (TC-04). The customer raises and lowers the quantity
    with the + and - buttons, finds the - button disabled at 1 (the minimum), and finally
    removes the tester, leaving an empty basket. The basket is seeded through the site's own
    add-to-cart API, so only the basket page is loaded and production is hit as little as possible.
    Given a desktop customer has a tester for shade "Romantic Reverie" in the basket
    When the customer increases the tester quantity
    Then the basket quantity is 2
    When the customer decreases the tester quantity
    Then the basket quantity is 1
    And the tester quantity cannot be decreased any further
    When the customer removes the tester from the basket
    Then the basket is empty

  @desktop @negative
  Scenario: Desktop customer is told when adding a tester to the basket fails
    Failure path (TC-05). The add-to-basket request is stubbed to fail in the browser, so it never
    reaches production. The customer must be shown an error message rather than the "added to your
    cart" confirmation, and the basket must stay empty. The message is short-lived (it fades after
    about three seconds), so it is asserted as soon as it appears.
    Given a desktop customer starts with an empty basket
    When the customer browses to shade "Romantic Reverie" from colour family "Violet"
    And the add-to-basket request fails
    And the customer tries to add a tester to the basket
    Then the customer is told something went wrong
    And the customer is not told the tester was added
    And the basket is still empty

  @desktop
  Scenario Outline: Desktop customer adds a tester for a shade from another colour family
    Catalogue coverage (TC-13). The purchase path does not depend on the one pinned shade: shades
    from other colour families are found through the colour finder and added to the basket the same
    way. Failing here while TC-01 passes points at that family or shade, not at the purchase flow.
    Given a desktop customer starts with an empty basket
    When the customer browses to shade "<shade>" from colour family "<colour_family>"
    And the customer adds a tester to the basket
    Then the basket contains 1 item
    And the basket includes tester "Dulux Colour Tester" for shade "<shade>"

    Examples:
      | colour_family | shade        |
      | Blue          | Breton Blue  |
      | Green         | Fresh Sage   |

  @smoke @desktop
  Scenario: Desktop customer sees the price of a tester and the order total
    Pricing (TC-14). One tester costs 2.90, delivery adds 1.50, so the order total is 4.40. The
    basket is seeded through the site's own add-to-cart API, so only the basket page is loaded.
    The amounts are production prices: a failure means the price changed, which is worth knowing.
    Given a desktop customer has a tester for shade "Romantic Reverie" in the basket
    Then the basket shows the tester price "£2.90", delivery "£1.50" and order total "£4.40"

  @desktop
  Scenario: Desktop customer finds the basket unchanged after reloading the page
    Basket persistence (TC-15). The basket lives in the session, not in the page: after a reload
    the customer still has the same tester, in the same quantity. The basket is seeded through the
    site's own add-to-cart API.
    Given a desktop customer has a tester for shade "Romantic Reverie" in the basket
    When the customer increases the tester quantity
    And the customer reloads the basket page
    Then the basket quantity is 2
    And the basket includes tester "Dulux Colour Tester" for shade "Romantic Reverie"

  @smoke @desktop
  Scenario: Desktop customer can open a shade from the colour finder
    Colour finder health check (TC-16). The customer reaches a shade through the top navigation
    and is offered a tester to buy. Nothing is added to the basket, so this is the cheapest check
    of the step that has proved timing-sensitive on other engines.
    Given a desktop customer starts with an empty basket
    When the customer browses to shade "Romantic Reverie" from colour family "Violet"
    Then the shade offers a tester to buy

  @smoke @desktop
  Scenario: Desktop customer with nothing in the basket is told so and can keep shopping
    Empty basket (TC-17). A first-time visitor who opens the basket sees that it is empty and is
    offered a way back to the products. Only the basket page is loaded.
    Given a desktop customer starts with an empty basket
    When the customer opens the basket
    Then the basket is empty
    And the customer is offered a way to continue shopping

  @smoke @desktop
  Scenario: Desktop customer can leave the basket and keep shopping
    Leaving the basket (TC-18). "Continue shopping" takes a customer with a tester in the basket
    to the product listing without losing the basket. The basket is seeded through the site's own
    add-to-cart API.
    Given a desktop customer has a tester for shade "Romantic Reverie" in the basket
    When the customer chooses to continue shopping
    Then the customer is on the products page

  @smoke @mobile
  Scenario: Mobile customer sees the tester in the basket
    The basket page on a phone (TC-22). A tester put in the basket through the site's own add-to-cart
    API is shown with its name, shade, quantity and price at 375 px wide. Only the basket page is loaded.
    Given a mobile customer has a tester for shade "Romantic Reverie" in the basket
    Then the basket contains 1 item
    And the basket includes tester "Dulux Colour Tester" for shade "Romantic Reverie"
    And the basket shows the tester price "£2.90", delivery "£1.50" and order total "£4.40"

  @smoke @tablet
  Scenario: Tablet customer sees the tester in the basket
    The same basket check on a tablet (TC-23), at 768 px wide.
    Given a tablet customer has a tester for shade "Romantic Reverie" in the basket
    Then the basket contains 1 item
    And the basket includes tester "Dulux Colour Tester" for shade "Romantic Reverie"
    And the basket shows the tester price "£2.90", delivery "£1.50" and order total "£4.40"
