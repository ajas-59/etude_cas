from playwright.sync_api import Page, expect, sync_playwright, Playwright
from test_connexion import connexion

def test_panier(page: Page) -> None:
    connexion(page)
    page.locator("[data-test=\"add-to-cart-sauce-labs-backpack\"]").click()
    page.locator("[data-test=\"shopping-cart-link\"]").click()
    
    # product text 
    expect(page.get_by_text("Sauce Labs Backpackcarry.")).to_be_visible()
    # remove bien en rouge
    #page.locator("[data-test=\"add-to-cart-sauce-labs-backpack\"]").click()
    expect(page.locator("[data-test=\"remove-sauce-labs-backpack\"]")).to_have_text("Remove")

    # icone panier affiche bien 1
    expect(page.locator("[data-test=\"shopping-cart-link\"]")).to_have_text("1")

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