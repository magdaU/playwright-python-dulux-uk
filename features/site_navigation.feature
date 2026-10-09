@regression
Feature: Use the Dulux site
  To find a colour quickly and get on with browsing
  As a Dulux customer
  I want site search to work and the cookie banner not to get in my way

  @smoke @desktop
  Scenario: Desktop customer sees the main navigation on the home page
    Home page health check (TC-12). A first-time visitor who has answered the cookie banner must
    find the three entry points every journey starts from: the colour finder, site search and the
    shopping cart. Only the home page is loaded.
    Given a desktop customer is on the home page
    Then the main navigation offers the colour finder, site search and the shopping cart

  @desktop @search
  Scenario Outline: Desktop customer searches for a shade
    Site search (TC-09). A known shade is found and shown on the results page; a term that matches
    nothing gets the site's "no results" message instead of an empty or broken page.
    Given a desktop customer is on the home page
    When the customer searches for "<term>"
    Then the search results are for "<term>"
    And the results show "<result>"

    @smoke
    Examples: the smoke pair
      | term             | result                                                  | rule                       |
      | Romantic Reverie | Romantic Reverie                                        | known shade is found       |
      | zzqqxxnoshade    | Sorry, we couldn't find any results for 'zzqqxxnoshade' | unknown term finds nothing |

    Examples: how the term is typed
      | term             | result           | rule                              |
      | romantic reverie | Romantic Reverie | search ignores letter case        |
      | Reverie          | Romantic Reverie | part of a name finds the shade    |

  @smoke @desktop @cookies
  Scenario: Desktop customer cannot use the site until the cookie banner is answered
    Cookie consent (TC-10). On a first visit the banner covers the page, so the navigation behind
    it cannot be used. After "Reject all" the banner is gone and the navigation works again.
    Given a desktop customer opens the home page without answering the cookie banner
    Then the cookie banner is shown
    And the navigation behind the banner cannot be used
    When the customer rejects all cookies
    Then the cookie banner is gone
    And the navigation can be used

  @mobile @cookies
  Scenario: Mobile customer answers the cookie banner
    Cookie consent on a phone (TC-19). On a first visit the banner is shown; after "Reject all" it is
    gone. The navigation behind the banner is not checked here: on mobile it is the hamburger menu.
    Given a mobile customer opens the home page without answering the cookie banner
    Then the cookie banner is shown
    When the customer rejects all cookies
    Then the cookie banner is gone

  @smoke @mobile
  Scenario: Mobile customer sees the menu on the home page
    Home page health check on a phone (TC-20). The navigation collapses into the hamburger menu, so
    the customer must find the menu, site search and the shopping cart. Only the home page is loaded.
    Given a mobile customer is on the home page
    Then the responsive navigation offers the menu, site search and the shopping cart

  @smoke @tablet
  Scenario: Tablet customer sees the menu on the home page
    The same health check on a tablet (TC-21), where the site also uses the hamburger menu.
    Given a tablet customer is on the home page
    Then the responsive navigation offers the menu, site search and the shopping cart
