from playwright.sync_api import Page, expect

from aides import connexion, panier_checkout


# --- Cas normal

def test_paiement(page: Page) -> None:
    # K1 : une commande complète aboutit au message de confirmation
    connexion(page)
    panier_checkout(page)

    page.locator('[data-test="firstName"]').fill("Jeanne")
    page.locator('[data-test="lastName"]').fill("Martin")
    page.locator('[data-test="postalCode"]').fill("35000")
    page.locator('[data-test="continue"]').click()
    page.locator('[data-test="finish"]').click()

    expect(page.locator('[data-test="complete-header"]')).to_have_text("Thank you for your order!")


# --- Cas d'erreur -----------------------------------------------------------

def test_first_name(page: Page) -> None:
    # K2 : prénom manquant
    connexion(page)
    panier_checkout(page)

    page.locator('[data-test="lastName"]').fill("Martin")
    page.locator('[data-test="postalCode"]').fill("35000")
    page.locator('[data-test="continue"]').click()

    expect(page.locator('[data-test="error"]')).to_contain_text("Error: First Name is required")


def test_last_name(page: Page) -> None:
    # K3 : nom manquant
    connexion(page)
    panier_checkout(page)

    page.locator('[data-test="firstName"]').fill("Jeanne")
    page.locator('[data-test="postalCode"]').fill("35000")
    page.locator('[data-test="continue"]').click()

    expect(page.locator('[data-test="error"]')).to_contain_text("Error: Last Name is required")


def test_postcode(page: Page) -> None:
    # K4 : code postal manquant
    connexion(page)
    panier_checkout(page)

    page.locator('[data-test="firstName"]').fill("Jeanne")
    page.locator('[data-test="lastName"]').fill("Martin")
    page.locator('[data-test="continue"]').click()

    expect(page.locator('[data-test="error"]')).to_contain_text("Error: Postal Code is required")
