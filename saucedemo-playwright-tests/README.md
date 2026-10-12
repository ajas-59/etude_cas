# Tests automatisés de SauceDemo avec Playwright

Suite de tests de bout en bout du site de démonstration
[saucedemo.com](https://www.saucedemo.com/), écrite en Python avec Playwright et pytest.
Elle couvre le parcours d'achat critique (connexion, panier, paiement), avec ses cas
normaux et ses cas d'erreur, et documente une anomalie détectée.

**Outils :** Python 3.11 · Playwright · pytest · pytest-playwright · GitHub Actions

## Lancer les tests

```bash
pip install -r requirements.txt
playwright install chromium
pytest -v
```

Pour voir le navigateur pendant l'exécution :

```bash
pytest --headed --slowmo 500
```

Les tests sont lancés automatiquement par GitHub Actions à chaque envoi de code
(voir `.github/workflows/tests.yml`).

## Organisation du projet

```
├── conftest.py          # fixture qui ouvre le site avant chaque test
├── aides.py             # fonctions de préparation : connexion, passage en commande
├── test_connexion.py    # cas C1 à C7
├── test_panier.py       # cas P1 à P4
├── test_paiement.py     # cas K1 à K4
└── .github/workflows/   # intégration continue
```

## Cas de test

### Connexion (`test_connexion.py`)

| N° | Cas de test | Résultat attendu | Test automatisé | Statut |
|----|-------------|------------------|-----------------|--------|
| C1 | Connexion avec identifiants valides | La liste des produits s'affiche | `test_connexion` | Réussi |
| C2 | Aucun champ saisi | Message « Username is required » | `test_sans_saisir` | Réussi |
| C3 | Identifiant vide, mot de passe valide | Message « Username is required » | `test_nom_utilisateur_vide` | Réussi |
| C4 | Identifiant valide, mot de passe vide | Message « Password is required » | `test_mdp_vide` | Réussi |
| C5 | Identifiant inconnu, mot de passe valide | Message « Username and password do not match any user in this service » | `test_nom_utilisateur_faux` | Réussi |
| C6 | Identifiant valide, mot de passe incorrect | Message « Username and password do not match any user in this service » | `test_mdp_faux` | Réussi |
| C7 | Identifiant et mot de passe incorrects | Message « Username and password do not match any user in this service » | `test_utilisateur_et_mdp_faux` | Réussi |

### Panier (`test_panier.py`)

| N° | Cas de test | Résultat attendu | Test automatisé | Statut |
|----|-------------|------------------|-----------------|--------|
| P1 | Ajout d'un article au panier | Le bouton affiche « Remove », le compteur affiche 1, l'article est dans le panier | `test_panier` | Réussi |
| P2 | Ajout puis retrait d'un article | Le bouton « Add to cart » réapparaît et le compteur disparaît | `test_add_remove_panier` | Réussi |
| P3 | Ajout d'un article, déconnexion, reconnexion | L'article est conservé dans le panier | `test_co_deco_panier` | Réussi |
| P4 | Commande avec un panier vide | La commande est refusée, l'utilisateur reste sur la page du panier | `test_panier_vide` | Échec attendu : anomalie n° 1 |

### Paiement (`test_paiement.py`)

| N° | Cas de test | Résultat attendu | Test automatisé | Statut |
|----|-------------|------------------|-----------------|--------|
| K1 | Commande complète avec un article | Message « Thank you for your order! » | `test_paiement` | Réussi |
| K2 | Prénom manquant | Message « Error: First Name is required » | `test_first_name` | Réussi |
| K3 | Nom manquant | Message « Error: Last Name is required » | `test_last_name` | Réussi |
| K4 | Code postal manquant | Message « Error: Postal Code is required » | `test_postcode` | Réussi |

Le test P4 est marqué "XFAIL (Anomalie n° 1 : le site autorise la commande d'un panier vide)", ce qui documente l'anomalie sans bloquer l'intégration continue.
Si l'anomalie était corrigée, il apparaîtrait comme `xpassed`.

## Anomalies détectées

### Anomalie n° 1 : commande possible avec un panier vide

| | |
|---|---|
| **Gravité** | Majeure |
| **Compte** | `standard_user` |
| **Étapes pour reproduire** | 1. Se connecter. 2. Ouvrir le panier sans ajouter d'article. 3. Cliquer sur « Checkout », remplir le formulaire, puis cliquer sur « Continue » et « Finish ». |
| **Résultat attendu** | La commande est impossible tant que le panier est vide. |
| **Résultat obtenu** | Le formulaire de commande s'ouvre et la commande peut être validée jusqu'au message de confirmation. |
| **Suggestion** | Désactiver ou masquer le bouton « Checkout » lorsque le panier est vide. |
| **Test associé** | `test_panier_vide` (P4) |

## Interprétation

Le panier est la fonctionnalité où les tests ont révélé des écarts : une anomalie et
une règle de fonctionnement à clarifier.

**Anomalie (P4).** Il est possible de passer commande avec un panier vide. Ce scénario
ne devrait pas être autorisé (voir l'anomalie n° 1).

**Règle à clarifier (P3).** Après ajout d'un article, déconnexion puis reconnexion,
l'article est conservé dans le panier. En l'absence de spécification, ce comportement
a été retenu comme résultat attendu. Il reste à confirmer auprès de l'équipe produit.

## Démarche

### Identification des fonctionnalités

Pour couvrir de façon systématique le parcours utilisateur, j'ai retenu trois
fonctionnalités critiques : la connexion, l'utilisation du panier et le paiement.

### Types de cas de test

Pour chacune, j'ai distingué deux types de situations :

- **Cas normaux** : l'utilisateur agit correctement, et l'application doit produire
  le résultat attendu.
- **Cas d'erreur** : l'utilisateur effectue une action invalide, et l'application
  doit la refuser en affichant un message.

| Type | Exemple | Résultat attendu |
|------|---------|------------------|
| Cas normal | L'utilisateur saisit un identifiant et un mot de passe valides | Il accède à la liste des produits |
| Cas d'erreur | L'utilisateur laisse le champ « Username » vide | La connexion est refusée, avec le message « Username is required » |

Chaque cas a d'abord été décrit dans un tableau (situation de départ, actions,
résultat attendu), puis automatisé. Les tableaux ci-dessus en sont la version à jour,
alignée sur les tests du dépôt.

## Choix techniques

### Fixture `page` plutôt que `playwright`

Mes premiers tests recevaient l'objet `playwright` en paramètre et ouvraient
eux-mêmes le navigateur. Cette approche présente deux inconvénients :

- **Fermeture non garantie.** Si une vérification échoue, le test s'arrête avant
  d'atteindre `browser.close()`, et le navigateur reste ouvert jusqu'à la fin de la
  session.
- **Code répétitif.** Chaque test doit lancer le navigateur, créer la page, puis tout
  fermer explicitement.

J'utilise désormais la fixture `page` du plugin pytest-playwright, qui ouvre et ferme
le navigateur autour de chaque test, qu'il réussisse ou qu'il échoue.

### Organisation du code

- Les tests sont regroupés par fonctionnalité, avec le cas normal en premier, puis les
  cas d'erreur.
- Chaque test est indépendant : il part d'un navigateur neuf et prépare lui-même sa
  situation de départ grâce aux fonctions de `aides.py`.
- La fixture de `conftest.py` ouvre le site avant chaque test.
- Les éléments sont ciblés par leurs attributs `data-test`, plus stables que leur
  position dans la page ou leur style.

## Leçon retenue : deux tests qui passaient à tort

En relisant mes tests, j'ai constaté que deux cas d'erreur de connexion (C5 et C6)
réussissaient sans vérifier le cas annoncé. Ils devaient tester des identifiants
incorrects, mais testaient en réalité un champ laissé vide.

**Cause.** Chaque test ne remplissait qu'un seul des deux champs. Le site affichait
donc « Password is required » ou « Username is required », et non le message attendu
pour des identifiants incorrects. Ma vérification, `to_be_visible()`, se contentait de
constater qu'un message d'erreur était affiché, quel qu'il soit.

**Conséquence.** Le cas « identifiants incorrects » figurait comme couvert dans mon
tableau alors qu'aucun test ne le vérifiait réellement.

**Correction.** Les deux champs sont désormais remplis, et chaque test vérifie le
texte précis du message :

```python
expect(page.locator('[data-test="error"]')).to_contain_text(
    "Username and password do not match any user in this service"
)
```

**Ce que j'en retiens.** Un test doit vérifier le contenu précis du résultat attendu,
et pas seulement sa présence. Une vérification trop vague peut laisser passer une
erreur dans le test lui-même.

## Limites et pistes d'amélioration

Cette étude se concentre sur trois fonctionnalités critiques du parcours d'achat.
Elle ne couvre pas :

- les autres pages et fonctions du site (tri des produits, fiche article, menu « About ») ;
- les autres comptes de démonstration, notamment `problem_user` ;
- d'autres navigateurs que Chromium ;
- les tests d'API.

Prochaines étapes envisagées : paramétrer les cas d'erreur de connexion en un seul
test, relancer la suite avec `problem_user` pour comparer les résultats, puis
l'exécuter sur Firefox.
