import pytest
from playwright.sync_api import Page, expect

from aides import connexion


# --- Cas normaux

def test_panier(page: Page) -> None:
    # P1 : l'ajout d'un article met à jour le bouton, le compteur et le panier
    connexion(page)

    page.locator('[data-test="add-to-cart-sauce-labs-backpack"]').click()

    expect(page.locator('[data-test="remove-sauce-labs-backpack"]')).to_have_text("Remove")
    expect(page.locator('[data-test="shopping-cart-badge"]')).to_have_text("1")

    page.locator('[data-test="shopping-cart-link"]').click()
    expect(page.locator("[data-test=\"item-4-title-link\"]")).to_have_text("Sauce Labs Backpack")
    
def test_add_remove_panier(page: Page) -> None:
    # P2 : après ajout puis retrait, le bouton « Add to cart » réapparaît
    connexion(page)

    page.locator('[data-test="add-to-cart-sauce-labs-backpack"]').click()
    page.locator('[data-test="remove-sauce-labs-backpack"]').click()

    expect(page.locator('[data-test="add-to-cart-sauce-labs-backpack"]')).to_be_visible()
    expect(page.locator('[data-test="shopping-cart-badge"]')).to_have_count(0)


def test_co_deco_panier(page: Page) -> None:
    """P3 : l'article est conservé dans le panier après déconnexion et reconnexion

    Résultat attendu retenu en l'absence de spécification : à confirmer
    auprès de l'équipe produit.
    """
    connexion(page)
    page.locator('[data-test="add-to-cart-sauce-labs-backpack"]').click()

    page.get_by_role("button", name="Open Menu").click()
    page.locator('[data-test="logout-sidebar-link"]').click()
    connexion(page)

    page.locator('[data-test="shopping-cart-link"]').click()
    expect(page.locator("[data-test=\"item-4-title-link\"]")).to_have_text("Sauce Labs Backpack")
    
# --- Cas d'erreur

@pytest.mark.xfail(reason="Anomalie n° 1 : le site autorise la commande d'un panier vide")
def test_panier_vide(page: Page) -> None:
    # P4 : il est impossible de commander avec un panier vide
    connexion(page)

    # ouvrir le panier sans avoir ajouté d'article, puis tenter de commander
    page.locator('[data-test="shopping-cart-link"]').click()
    page.locator('[data-test="checkout"]').click()

    # attendu : la commande est refusée, l'utilisateur reste sur le panier
    expect(page).to_have_url("https://www.saucedemo.com/cart.html")
