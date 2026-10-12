from playwright.sync_api import Page, expect

from aides import connexion

MESSAGE_IDENTIFIANTS_INCORRECTS = (
    "Username and password do not match any user in this service"
)


# --- Cas normal

def test_connexion(page: Page) -> None:
    # C1 : identifiants valides donnent accès à la liste des produits
    connexion(page)

    expect(page.locator('[data-test="inventory-container"]')).to_be_visible()


# --- Cas d'erreur

def test_sans_saisir(page: Page) -> None:
    # C2 : aucun champ saisi
    page.locator('[data-test="login-button"]').click()

    expect(page.locator('[data-test="error"]')).to_contain_text("Username is required")


def test_nom_utilisateur_vide(page: Page) -> None:
    # C3 : identifiant vide, mot de passe valide
    connexion(page, identifiant="")

    expect(page.locator('[data-test="error"]')).to_contain_text("Username is required")


def test_mdp_vide(page: Page) -> None:
    # C4 : identifiant valide, mot de passe vide
    connexion(page, mot_de_passe="")

    expect(page.locator('[data-test="error"]')).to_contain_text("Password is required")


def test_nom_utilisateur_faux(page: Page) -> None:
    # C5 : identifiant inconnu, mot de passe valide
    connexion(page, identifiant="standard")

    expect(page.locator('[data-test="error"]')).to_contain_text(MESSAGE_IDENTIFIANTS_INCORRECTS)


def test_mdp_faux(page: Page) -> None:
    # C6 : identifiant valide, mot de passe incorrect
    connexion(page, mot_de_passe="secret")

    expect(page.locator('[data-test="error"]')).to_contain_text(MESSAGE_IDENTIFIANTS_INCORRECTS)


def test_utilisateur_et_mdp_faux(page: Page) -> None:
    # C7 : identifiant et mot de passe incorrects
    connexion(page, identifiant="standard", mot_de_passe="secret")

    expect(page.locator('[data-test="error"]')).to_contain_text(MESSAGE_IDENTIFIANTS_INCORRECTS)
