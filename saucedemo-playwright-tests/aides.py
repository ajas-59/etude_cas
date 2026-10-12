# fonctions d'aide partagées par les tests pour préparation des situations de départ 
from playwright.sync_api import Page


def connexion(
    page: Page,
    identifiant: str = "standard_user",
    mot_de_passe: str = "secret_sauce",
) -> None:
    #connexion depuis la page de connexion (ouverte par la fixture de conftest.py)
    page.locator('[data-test="username"]').fill(identifiant)
    page.locator('[data-test="password"]').fill(mot_de_passe)
    page.locator('[data-test="login-button"]').click()


def panier_checkout(page: Page) -> None:
    # ajouter un article au panier, ouvrir le panier et lancer la commande
    page.locator('[data-test="add-to-cart-sauce-labs-backpack"]').click()
    page.locator('[data-test="shopping-cart-link"]').click()
    page.locator('[data-test="checkout"]').click()
