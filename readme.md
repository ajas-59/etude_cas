# Cas d'étude : saucedemo.com avec Playwright

Site étudié : https://www.saucedemo.com/

## Démarche

### Identification des fonctionnalités

Pour couvrir de façon systématique les parcours utilisateur, j'ai d'abord retenu
trois fonctionnalités :

1. la connexion de l'utilisateur ;
2. l'utilisation du panier ;
3. le paiement.

### Types de cas de test

Pour chacune, j'ai distingué deux types de situations :

- **Cas normaux** : l'utilisateur agit correctement, et l'application doit produiren le résultat attendu.
- **Cas d'erreur** : l'utilisateur effectue une action invalide, et l'application doit la refuser en affichant un message.

| Type | Exemple | Résultat attendu |
|------|---------|------------------|
| Cas normal | L'utilisateur saisit un identifiant et un mot de passe valides | Il accède à la liste des produits |
| Cas d'erreur | L'utilisateur laisse le champ « Username » vide | La connexion est refusée, avec le message « Username is required » |

### Rédaction des cas

Chaque cas a été décrit dans un tableau avant d'être automatisé : situation de départ,
actions à réaliser, résultat attendu. Le tableau présenté plus bas en est la version
à jour, alignée sur les tests du dépôt.

## Choix techniques

### Fixture `page` plutôt que `playwright`

Mes premiers tests recevaient l'objet `playwright` en paramètre et ouvraient
eux-mêmes le navigateur. Cette approche présente deux inconvénients :

- **Fermeture non garantie.** Si une vérification échoue, le test s'arrête avant
  d'atteindre `browser.close()`. Les navigateurs restés ouverts consomment de la
  mémoire jusqu'à la fin de la session.
- **Code répétitif.** Chaque test doit lancer le navigateur, créer la page, puis
  tout fermer explicitement.

J'utilise désormais la fixture `page` du plugin pytest-playwright, qui ouvre et
ferme le navigateur autour de chaque test, qu'il réussisse ou qu'il échoue.

### Organisation du code

Les tests étaient d'abord répartis selon les deux types de situations. Leur nombre
augmentant, je les ai regroupés par fonctionnalité, avec un fichier pour la
connexion, un pour le panier et un pour le paiement.

Le fichier `conftest.py` contient une fixture exécutée avant chaque test, qui ouvre
le site à tester.

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

Le panier est la fonctionnalité où les tests ont révélé des écarts : une anomalie et une règle de fonctionnement à clarifier.

**Anomalie (P4).** Il est possible de passer commande avec un panier vide, jusqu'au
message de confirmation. Ce scénario ne devrait pas être autorisé.
Voir le rapport d'anomalie n° 1.

**Règle à clarifier (P3).** Après ajout d'un article, déconnexion puis reconnexion, l'article est conservé dans le panier. En l'absence de spécification, ce comportement a été retenu comme résultat attendu. Il reste à confirmer auprès de l'équipe produit.

## Limites et pistes d'amélioration

Cette étude se concentre sur trois fonctionnalités critiques du parcours d'achat :
la connexion, le panier et le paiement.

Elle ne couvre pas :

- les autres pages et fonctions du site (tri des produits, fiche article, menu « About ») ;
- les autres comptes de démonstration, notamment `problem_user` ;
- d'autres navigateurs que Chromium ;
- les tests d'API.

Prochaines étapes envisagées : relancer la suite avec `problem_user` pour comparer
les résultats, puis l'exécuter sur Firefox.


## Leçon retenue : deux tests qui passaient à tort

En relisant mes tests, j'ai constaté que deux cas d'erreur de connexion (C5 et C6)
réussissaient sans vérifier le cas annoncé. Ils devaient tester des identifiants
incorrects, mais testaient en réalité un champ laissé vide.

**Cause.** Chaque test ne remplissait qu'un seul des deux champs. Le site affichait
donc « Password is required » ou « Username is required », et non le message attendu
pour des identifiants incorrects. Ma vérification, `to_be_visible()`, se contentait
de constater qu'un message d'erreur était affiché, quel qu'il soit.

**Conséquence.** Le cas « identifiants incorrects » figurait comme couvert dans mon
tableau alors qu'aucun test ne le vérifiait réellement.

**Correction.** Les deux champs sont désormais remplis, et chaque test vérifie le
texte précis du message :

​```python
expect(page.locator('[data-test="error"]')).to_contain_text(
    "Username and password do not match any user in this service"
)
​```

**Ce que j'en retiens.** Un test doit vérifier le contenu précis du résultat attendu,
et pas seulement sa présence. Une vérification trop vague peut laisser passer une
erreur dans le test lui-même.
