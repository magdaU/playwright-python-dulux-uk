@regression
Feature: Use the Dulux site
  To find a colour quickly and get on with browsing
  As a Dulux customer
  I want site search to work and the cookie banner not to get in my way

  @desktop @search
  Scenario Outline: Desktop customer searches for a shade
    Site search (TC-09). A known shade is found and shown on the results page; a term that matches
    nothing gets the site's "no results" message instead of an empty or broken page.
    Given a desktop customer is on the home page
    When the customer searches for "<term>"
    Then the search results are for "<term>"
    And the results show "<result>"

    Examples:
      | term             | result                                                  | rule                       |
      | Romantic Reverie | Romantic Reverie                                        | known shade is found       |
      | zzqqxxnoshade    | Sorry, we couldn't find any results for 'zzqqxxnoshade' | unknown term finds nothing |

  @desktop @cookies
  Scenario: Desktop customer cannot use the site until the cookie banner is answered
    Cookie consent (TC-10). On a first visit the banner covers the page, so the navigation behind
    it cannot be used. After "Reject all" the banner is gone and the navigation works again.
    Given a desktop customer opens the home page without answering the cookie banner
    Then the cookie banner is shown
    And the navigation behind the banner cannot be used
    When the customer rejects all cookies
    Then the cookie banner is gone
    And the navigation can be used
