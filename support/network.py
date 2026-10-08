"""Keep test browsers off traffic that adds load and time but is irrelevant to what is tested.

One purchase journey sends roughly 300 requests, and only about a fifth of them go to
dulux.co.uk: the rest is analytics, tag managers, live chat, monitoring and captcha scripts. Blocking
those makes every scenario faster and lighter on production, and the tests assert nothing
about them. The consent banner's own host (cdn.cookielaw.org), fonts and images are
deliberately left alone, so the cookie scenario and the accessibility scan still see the
real page.
"""

from urllib.parse import urlparse

from playwright.sync_api import BrowserContext, Route

BLOCKED_HOSTS = frozenset(
    {
        "aodp.dulux.co.uk",  # first-party analytics pixel
        "www.googletagmanager.com",
        "assets.adobedtm.com",
        "webchat.asksid.ai",  # live chat
        "thumb.sprinklr.com",
        "gallery.sprinklr.com",
        "www.recaptcha.net",
        "www.gstatic.com",  # captcha assets (fonts live on fonts.gstatic.com, not blocked)
        "js-agent.newrelic.com",  # performance monitoring
        "bam.nr-data.net",
    }
)


def _block_if_noise(route: Route) -> None:
    if urlparse(route.request.url).hostname in BLOCKED_HOSTS:
        route.abort()
    else:
        route.fallback()


def block_third_party_noise(context: BrowserContext) -> None:
    context.route("**/*", _block_if_noise)
