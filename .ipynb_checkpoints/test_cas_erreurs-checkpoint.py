import re
from playwright.sync_api import Page, Playwright, sync_playwright, expect

# CAS ANORMAL
def test_connexion(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    
    page.goto("https://www.saucedemo.com/")
    #sit début : Username, mdp demandé et bouton login
  
    # 1. laisser les deux champs vides
    # Action : 
    # i. cliquer bouton "Login"
    # expect(message d'erreur : identifiant obligatoire)
    page.locator("[data-test=\"login-button\"]").click()
    expect(page.locator("[data-test=\"error\"]")).to_be_visible()

    # 2. laisser nom d'utilisateur vide
    # Actions : 
    # i. saisir secret_sauce en mdp
    # ii. cliquer bouton "Login"
    # expect(message d'erreur : identifiant obligatoire)
    page.locator("[data-test=\"password\"]").fill("secret_sauce")
    page.locator("[data-test=\"login-button\"]").click()
    expect(page.locator("[data-test=\"error\"]")).to_be_visible()

    # 3. laisser mot de passe vide
    # Actions : 
    # i. saisir "standard_user" en Username
    # ii. cliquer bouton "Login"
    # message d'erreur : mdp obligatoire
    page.locator("[data-test=\"username\"]").fill("standard_user")
    page.locator("[data-test=\"login-button\"]").click()
    expect(page.locator("[data-test=\"error\"]")).to_be_visible()

    # 4. mettre un nom d'utilisateur faux
    # Action : 
    # i. saisir "standard" en Username
    # ii. cliquer bouton "Login"
    # expect(message d'erreur : Username non reconnu)
    page.locator("[data-test=\"username\"]").fill("standard")
    page.locator("[data-test=\"login-button\"]").click()
    expect(page.locator("[data-test=\"error\"]")).to_be_visible()

    # 5. mettre un mdp faux
    # Action : 
    # i. saisir "secret" en mdp
    # ii. cliquer bouton "Login"
    # expect(message d'erreur : mdp non reconnu)
    page.locator("[data-test=\"password\"]").fill("secret")
    page.locator("[data-test=\"login-button\"]").click()
    expect(page.locator("[data-test=\"error\"]")).to_be_visible()


def test_panier(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    
    page.goto("https://www.saucedemo.com/")
    
    # se connecter normalement
    page.locator("[data-test=\"username\"]").fill("standard_user")
    page.locator("[data-test=\"password\"]").fill("secret_sauce")
    page.locator("[data-test=\"login-button\"]").click()
    
    # bouton ajouter puis enlever
    page.locator("[data-test=\"add-to-cart-sauce-labs-backpack\"]").click()
    page.locator("[data-test=\"remove-sauce-labs-backpack\"]").click()

    # passer au panier sans rien
    page.locator("[data-test=\"shopping-cart-link\"]").click()
    page.locator("[data-test=\"checkout\"]").click()

    # ajouter produit puis se déconnecter
    page.locator("[data-test=\"add-to-cart-sauce-labs-backpack\"]").click()
    page.get_by_role("button", name="Open Menu").click()
    page.locator("[data-test=\"logout-sidebar-link\"]").click()
    page.locator("[data-test=\"username\"]").fill("standard_user")
    page.locator("[data-test=\"password\"]").fill("secret_sauce")
    page.locator("[data-test=\"login-button\"]").click()
    page.locator("[data-test=\"shopping-cart-link\"]").click()
    page.get_by_text("Sauce Labs Backpackcarry.").click()


#def test_paiement(playwright: Playwright) -> None:

with sync_playwright() as playwright:
    test_connexion(playwright)
    test_panier(playwright)
    