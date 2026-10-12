from playwright.sync_api import Page, expect, sync_playwright, Playwright
from test_connexion import connexion

def panier_checkout(page: Page) -> None:
    page.locator("[data-test=\"add-to-cart-sauce-labs-backpack\"]").click()
    page.locator("[data-test=\"shopping-cart-link\"]").click()
    page.locator("[data-test=\"checkout\"]").click()


def test_paiement(page: Page) -> None:
    connexion(page)
    panier_checkout(page)

    # paiement commence
    page.locator("[data-test=\"firstName\"]").click()
    page.locator("[data-test=\"firstName\"]").fill("AZE")
    page.locator("[data-test=\"lastName\"]").click()
    page.locator("[data-test=\"lastName\"]").fill("zdz")
    page.locator("[data-test=\"postalCode\"]").click()
    page.locator("[data-test=\"postalCode\"]").fill("zdzd")
    page.locator("[data-test=\"continue\"]").click()
    page.locator("[data-test=\"finish\"]").click()
    expect(page.locator("[data-test=\"complete-text\"]")).to_be_visible()

# ne pas saisir First Name	message d'erreur : Error : First Name is required
def test_first_name (page: Page) -> None:
    connexion(page)
    panier_checkout(page)
    page.locator("[data-test=\"lastName\"]").fill("S")
    page.locator("[data-test=\"postalCode\"]").fill("75")
    page.locator("[data-test=\"continue\"]").click()
    expect(page.locator("[data-test=\"error\"]")).to_contain_text("Error: First Name is required")

# last name manquant
def test_last_name (page: Page) -> None:
    connexion(page)
    panier_checkout(page)
    page.locator("[data-test=\"firstName\"]").fill("Am")
    page.locator("[data-test=\"postalCode\"]").fill("75")
    page.locator("[data-test=\"continue\"]").click()
    expect(page.locator("[data-test=\"error\"]")).to_contain_text("Error: Last Name is required")

# postcode manquant
def test_postcode (page: Page) -> None:
    connexion(page)
    panier_checkout(page)
    page.locator("[data-test=\"firstName\"]").fill("Am")
    page.locator("[data-test=\"lastName\"]").fill("S")
    page.locator("[data-test=\"continue\"]").click()
    expect(page.locator("[data-test=\"error\"]")).to_contain_text("Error: Postal Code is required")