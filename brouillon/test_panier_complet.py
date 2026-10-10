import re
from playwright.sync_api import Page, Playwright, sync_playwright, expect

def connexion(page: Page) -> None:
    page.goto("https://www.saucedemo.com/")
    page.locator("[data-test=\"username\"]").fill("standard_user")
    page.locator("[data-test=\"password\"]").fill("secret_sauce")
    page.locator("[data-test=\"login-button\"]").click()
    
def test_connexion(page: Page) -> None:
    connexion(page)
    expect(page.locator("[data-test=\"inventory-container\"]")).to_be_visible()

def test_panier(page: Page) -> None:
    test_connexion(page)
    page.locator("[data-test=\"add-to-cart-sauce-labs-backpack\"]").click()
    page.locator("[data-test=\"shopping-cart-link\"]").click()
    # product text 
    expect(page.get_by_text("Sauce Labs Backpackcarry.")).to_be_visible()
    # remove bien en rouge
    #page.locator("[data-test=\"add-to-cart-sauce-labs-backpack\"]").click()
    expect(page.locator("[data-test=\"remove-sauce-labs-backpack\"]")).to_have_text("Remove")

    # icone panier affiche bien 1
    expect(page.locator("[data-test=\"shopping-cart-link\"]")).to_have_text("1")

def test_paiement(page: Page) -> None:
    test_panier(page)

    # paiement commence
    page.locator("[data-test=\"checkout\"]").click()
    page.locator("[data-test=\"firstName\"]").click()
    page.locator("[data-test=\"firstName\"]").fill("AZE")
    page.locator("[data-test=\"lastName\"]").click()
    page.locator("[data-test=\"lastName\"]").fill("zdz")
    page.locator("[data-test=\"postalCode\"]").click()
    page.locator("[data-test=\"postalCode\"]").fill("zdzd")
    page.locator("[data-test=\"continue\"]").click()
    page.locator("[data-test=\"finish\"]").click()
    expect(page.locator("[data-test=\"complete-text\"]")).to_be_visible()
    
# ouvir et fermer
# sync_playwright : fonction qui crée l'oject
#with sync_playwright() as playwright:
 #   test_connexion(playwright)