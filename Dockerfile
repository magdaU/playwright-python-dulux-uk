# syntax=docker/dockerfile:1

# Reproducible E2E test runner for the Dulux Playwright framework (Python).
# Mirrors the GitHub Actions pipeline: Python 3.12, Chromium installed with its
# OS dependencies, smoke suite run headless by default.
FROM python:3.12-slim

ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright \
    PYTEST_MARKERS=smoke

WORKDIR /app

# 1) Resolve dependencies first for better layer caching.
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 2) Install Chromium + the OS libraries it needs (apt requires root here).
RUN playwright install --with-deps chromium

# 3) Add the test sources.
COPY conftest.py pytest.ini ./
COPY pages ./pages
COPY features ./features
COPY tests ./tests

# 4) Run as a non-root user so Chromium's sandbox behaves exactly as it does on
#    the CI runner. The shared /app and /ms-playwright are handed to that user.
RUN useradd --create-home --uid 1001 pwuser \
    && chown -R pwuser:pwuser /app /ms-playwright
USER pwuser

# PYTEST_MARKERS can be overridden at run time, e.g.
#   docker run --rm -e PYTEST_MARKERS="regression" dulux-python-e2e-tests
CMD ["sh", "-c", "pytest -m \"${PYTEST_MARKERS}\" --alluredir=allure-results"]
