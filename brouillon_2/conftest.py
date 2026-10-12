import pytest

from playwright.sync_api import Page

@pytest.fixture(autouse=True)
def config(page: Page) -> None:
    page.goto("https://www.saucedemo.com/")