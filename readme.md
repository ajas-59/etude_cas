# Cas d'étude : https://www.saucedemo.com/ grâce à Playwright.

## Etude des fonctionalités et cas
Pour systématiquement comprendre l'ensemble des fonctionnalités et les chemins utilisateurs possibles nous avons commencé par trier les résultats attendus selon ces 3 fonctionnalités :

1) Connexion de l'utilisateur au site
2) Utilisation du panier
3) Paiement

Nous avons alors trié selon différentes types de situations :
- a) les cas où l'utilisateur a un comportement normal mais que le résultat attendu n'est pas retrouvé
- b) les cas où l'utilisateur à un comprtement anormal et que, dans ce contexte là, le résultat attendu n'est pas retrouvé

ex : 
a) Utilisateur remplit correctement les champs "Username" et "Password" -> mais il n'accède pas au site
b) Utilisateur remplit ne remplit pas le champ "Username" -> mais il accède pas au site

Pour ce faire, nous avons crée un tableau décrivant la situation de début, les actions à réaliser afin d'emprunter le même chemin et les résultats attendus. Le tableau à retrouver plus bas est la version mise à jour de ce dernier.


## Playwright et Page
Au premier essai j'ai utilisé Playwright comme paramètre au lieu de Page.

Ceci a pour désavantage que, en cas d'echec d'un test, le naviagateur n'est pas fermé car il n'atteint jamais le bloc "browser.close()"

Au fur à mesure des tests, du mémoire est alors utilisé en continu afin de garder ces navigateurs ouverts.

Encore, Playwright nécessite une définition plus détaillé afin d'appeller le Page nécessaire.
Ainsi que, une fermeture explicite du navigateur.

## Structurer
Nous avons tout d'abord structuré notre code par nos deux types de situation décrite plus haut (à retrouver dans /brouillon).
Toutefois, dû aux nombreux tests nous avons choisi de plutôt trier par fonctionnalité.

Nous avons également crée un fichier de configuration : conftest.py, qui contient le sité à tester.

## Tableau de résultats
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
| P1 | Ajout d'un article au panier | L'article apparaît dans le panier, le bouton affiche « Remove », le compteur affiche 1 | `test_panier` | Réussi |
| P2 | Ajout puis retrait d'un article | Le bouton « Add to cart » réapparaît | `test_add_remove_panier` | Réussi |
| P3 | Ajout d'un article, déconnexion, reconnexion | L'article est conservé dans le panier | `test_co_deco_panier` | Réussi |
| P4 | Commande avec un panier vide | La commande est refusée, l'utilisateur reste sur la page du panier | `test_panier_vide` | Échec : anomalie n° 1 |

### Paiement (`test_paiement.py`)

| N° | Cas de test | Résultat attendu | Test automatisé | Statut |
|----|-------------|------------------|-----------------|--------|
| K1 | Commande complète avec un article | Le message de confirmation s'affiche | `test_paiement` | Réussi |
| K2 | Prénom manquant | Message « Error: First Name is required » | `test_first_name` | Réussi |
| K3 | Nom manquant | Message « Error: Last Name is required » | `test_last_name` | Réussi |
| K4 | Code postal manquant | Message « Error: Postal Code is required » | `test_postcode` | Réussi |



## Interprétation
La fonctionnalité le plus à risque est le panier, avec un echec et un choix de fonctionnement ambigu.
En effet, nous avons rencontré un echec au test P4, à savoir, la possibilité de commander avec un panier vide. 
Ce scénario ne devrait pas être possible.

Nous aurons également à échanger avec l'équipe technique afin de vérifier le résultat attendu pour le test P3 : ajout d'un article, déconnexion, reconnexion. Nous devons vérfiier que nous souhaitons bien garder un article dans le panier même après déconnexion.

## Ouverture et limites
Nous n'avons pas réalisé des tests pour l'ensemble des fonctionnalités et pages du site tel que la page "Dynamic catalogue" ou "About" nous avons seulement choisi de cibler pour notre cas d'études trois qui sont critiques pour le bon déroulement de l'expérience utilisateur du site : la connexion, puis l'utilisation du panier et enfin le passage au paiement qui se situent sur la page de connexion, la page "All Items" ou "Products" sur lequel nous arrivons directement après connexion, et les pages liés au panier et paiement.

## Erreur lors de la conception des tests
En C5 et C6, tes tests passaient alors qu'ils ne vérifiaient pas le cas annoncé : ils voulaient tester des identifiants incorrects, mais testaient en réalité un champ laissé vide.

**Ce que le test était censé faire**

`test_nom_utilisateur_faux` devait saisir un identifiant inconnu avec un mot de passe valide, puis vérifier que le site refuse la connexion avec le message « identifiants incorrects ».

**Ce qu'il faisait réellement**

```python
def test_nom_utilisateur_faux(page: Page) -> None:
    page.locator('[data-test="username"]').fill("standard")     # identifiant saisi
                                                                 # mot de passe : jamais saisi
    page.locator('[data-test="login-button"]').click()
    expect(page.locator('[data-test="error"]')).to_be_visible()
```

1. Le test saisit l'identifiant « standard », mais aucun mot de passe.
2. Le site constate que le mot de passe est vide et s'arrête là. Il affiche « Password is required », sans même examiner l'identifiant.
3. Le test vérifie seulement qu'un message d'erreur est visible. Il y en a bien un, donc il réussit.

C6 est le cas symétrique : le mot de passe est saisi, pas l'identifiant, et le site répond « Username is required ».

**Les deux causes**

- **Une donnée manquante** dans la préparation du test : un seul des deux champs était rempli.
- **Une vérification trop vague** : `to_be_visible()` accepte n'importe quel message d'erreur. C'est elle qui a laissé passer l'oubli.

**La conséquence**

Le cas « identifiants incorrects » n'était en réalité testé par aucun de ces deux tests, alors que ton tableau l'affichait comme couvert. Si le site avait cessé de rejeter les mauvais identifiants, C5 et C6 seraient restés verts. C'est ce qu'on appelle un **faux négatif** : un test qui passe sans protéger contre le défaut qu'il est censé détecter.

**La correction**

Remplir les deux champs, et vérifier le texte précis du message. Avec cette seule vérification précise, le test aurait échoué dès le départ et révélé l'oubli.

**En conclusion**

En relisant mes tests, j'ai vu que deux cas d'erreur passaient pour une mauvaise raison : il manquait une donnée, et ma vérification se contentait de constater qu'un message d'erreur était affiché. Ceci souligne l'importance de toujours toujours vérifier le contenu précis du résultat attendu, et pas seulement sa présence.