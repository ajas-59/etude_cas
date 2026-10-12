import pytest
from playwright.sync_api import Page

URL_SITE = "https://www.saucedemo.com/"


@pytest.fixture(autouse=True)
def ouvrir_site(page: Page) -> None:
    """Ouvre la page de connexion de SauceDemo avant chaque test."""
    page.goto(URL_SITE)
