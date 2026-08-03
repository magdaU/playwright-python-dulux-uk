import logging
from typing import Callable

import allure

logger = logging.getLogger(__name__)


class RetryExhaustedError(Exception):
    """Raised when a bounded retry never succeeded."""


def retry(action: Callable[[], None], *, attempts: int, description: str) -> None:
    """Retry a known-flaky interaction a bounded number of times.

    Only for steps we've specifically identified as flaky (see
    docs/TEST_STRATEGY.md S10, "Cross-engine navigation timing") — not a
    blanket wrapper for every step. Every failed attempt, and a success that
    only happened on a retry, is logged AND attached to the Allure report so
    a passing run is never silently indistinguishable from a clean one.
    """
    last_error: Exception | None = None
    for attempt in range(1, attempts + 1):
        try:
            action()
            if attempt > 1:
                _report(f'"{description}" succeeded on retry attempt {attempt}/{attempts}')
            return
        except Exception as error:
            last_error = error
            if attempt < attempts:
                _report(
                    f'"{description}" failed on attempt {attempt}/{attempts} '
                    f"({error.__class__.__name__}), retrying"
                )

    raise RetryExhaustedError(
        f'"{description}" did not succeed after {attempts} attempts'
    ) from last_error


def _report(message: str) -> None:
    logger.warning(message)
    allure.attach(message, name="Retry", attachment_type=allure.attachment_type.TEXT)
