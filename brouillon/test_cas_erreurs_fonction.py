# CAS ANORMAUX BON
from playwright.sync_api import Page, expect, sync_playwright, Playwright

# tests connexion
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


# test panier
def connexion (page: Page) -> None:
    page.locator("[data-test=\"username\"]").fill("standard_user")
    page.locator("[data-test=\"password\"]").fill("secret_sauce")
    page.locator("[data-test=\"login-button\"]").click()
    
def test_add_remove_panier (page: Page) -> None:
    connexion(page)
    
    # bouton ajouter puis enlever
    page.locator("[data-test=\"add-to-cart-sauce-labs-backpack\"]").click()
    page.locator("[data-test=\"remove-sauce-labs-backpack\"]").click()
    expect(page.locator("[data-test=\"add-to-cart-sauce-labs-backpack\"]")).to_be_visible()

def test_co_deco_panier (page: Page) -> None:
    connexion(page)
    # ajouter produit puis se déconnecter
    page.locator("[data-test=\"add-to-cart-sauce-labs-backpack\"]").click()
    page.get_by_role("button", name="Open Menu").click()
    page.locator("[data-test=\"logout-sidebar-link\"]").click()
    
    connexion(page)
    
    page.locator("[data-test=\"shopping-cart-link\"]").click()
    expect(page.get_by_text("Sauce Labs Backpackcarry.")).to_be_visible()

def test_panier_vide (page: Page) -> None:
    connexion(page)
    
    # passer au panier sans rien, ne pas pouvoir mettre ses infos perso
    page.locator('[data-test="shopping-cart-link"]').click()
    page.locator('[data-test="checkout"]').click()

    # Attendu : on reste sur le panier car utilisateur pas le droit d'avancer
    expect(page).to_have_url("https://www.saucedemo.com/cart.html")
    
# tests paiement
def panier_checkout (page: Page) -> None:
    page.locator("[data-test=\"add-to-cart-sauce-labs-backpack\"]").click()
    page.locator("[data-test=\"shopping-cart-link\"]").click()
    page.locator("[data-test=\"checkout\"]").click()

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