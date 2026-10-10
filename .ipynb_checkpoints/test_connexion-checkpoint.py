from playwright.sync_api import Page, expect, sync_playwright, Playwright


def connexion(page: Page) -> None:
    page.goto("https://www.saucedemo.com/")
    page.locator("[data-test=\"username\"]").fill("standard_user")
    page.locator("[data-test=\"password\"]").fill("secret_sauce")
    page.locator("[data-test=\"login-button\"]").click()

def test_connexion(page: Page) -> None:
    connexion(page)
    expect(page.locator("[data-test=\"inventory-container\"]")).to_be_visible()

def test_sans_saisir (page: Page) -> None:
    page.locator("[data-test=\"login-button\"]").click()
    expect(page.locator("[data-test=\"error\"]")).to_contain_text("Username is required")
    
def test_nom_utilisateur_vide (page: Page) -> None:
    page.locator("[data-test=\"password\"]").fill("secret_sauce")
    page.locator("[data-test=\"login-button\"]").click()
    expect(page.locator("[data-test=\"error\"]")).to_contain_text("Username is required")

def test_mdp_vide (page: Page) -> None:
    page.locator("[data-test=\"username\"]").fill("standard_user")
    page.locator("[data-test=\"login-button\"]").click()
    expect(page.locator("[data-test=\"error\"]")).to_contain_text("Password is required")

def test_nom_utilisateur_faux (page: Page) -> None:
    page.locator("[data-test=\"username\"]").fill("standard")
    page.locator("[data-test=\"password\"]").fill("secret_sauce")
    page.locator("[data-test=\"login-button\"]").click()
    expect(page.locator("[data-test=\"error\"]")).to_contain_text("Username and password do not match any user in this service")

def test_mdp_faux (page: Page) -> None:
    page.locator("[data-test=\"username\"]").fill("standard_user")
    page.locator("[data-test=\"password\"]").fill("secret")
    page.locator("[data-test=\"login-button\"]").click()
    expect(page.locator("[data-test=\"error\"]")).to_contain_text("Username and password do not match any user in this service")

def test_utilisateur_et_mdp_faux (page: Page) -> None:
    page.locator("[data-test=\"username\"]").fill("standard")
    page.locator("[data-test=\"password\"]").fill("secret")
    page.locator("[data-test=\"login-button\"]").click()
    expect(page.locator("[data-test=\"error\"]")).to_contain_text("Username and password do not match any user in this service")