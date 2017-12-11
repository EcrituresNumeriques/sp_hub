# Spécifications éditoriales

## Correspondance "Rubriques"

SPIP                              | HUB                       | Erudit
:---------------------------------|:--------------------------|:-----------
_correspond à l'objet "Rubrique"_ | _typeObjet_>_typeArticle_ |
Essais      (rub. 58)             | article>essai             | article
Créations   (rub. 60)             | article>créations         | autre
Lecture     (rub. 76)             | article>lecture           | compterendu
Actes       (rub. 107)            | conversation              | -
Dossiers    (rub. 109)            | conversation              | -
Entretiens  (rub. 113)            | article>entretien         | autre
Chroniques  (rub. 114)            | article>chronique         | autre


## Correspondance "Vocabulaire contrôlé" (pour les mots-clés éditeurs)

SPIP                      | HUB                | Erudit
:-------------------------|:-------------------|:------
Regroupements thématiques | sujet              | -
Auteurs principaux cités  | auteur             | -
Thématiques               | v0: thématique   <br/> v1: catégorie "calculée"      | -
Régions                   | région             | -
Tags domaines artistiques | domaine artistique | -

Concernant les Thématiques, voici [ce qui était prévu](https://github.com/timoguic/sp_hub/blob/master/doc/20170914_RecapReunion9sept.md#th%C3%A9matiques). Précisions :

Dans Spip, le vocabulaire contrôlé "Thématiques" classaient les articles en 6 thématiques représentant les champs d'étude de la revue. Ces Thématiques étaient renseignées comme mot-clé.

Pour le Hub, on souhaite conserver les thématiques davantage comme des catégories. Le principe consiste à considérer ces catégories à partir du champ sémantique des mots-clés éditeurs. Ainsi, les 6 thématiques seront plus souples et non-exclusives.

Déploiement : Dans un v0, on conserve la donnée "thématique" "en dur", c'est-à-dire comme un mot-clé.
Puis, une fois que le corpus d'article sera suffisant, on pourra extraire le champ sémantique de chaque thématique. Ensuite, pour un nouvel article, il sera possible d'identifier sa ou ses catégorie.s à partir de ses mots-clés et de leur proximité au champ sémantique de chaque thématique (catégorie.s calculée.s).

Exploitation: on implémente les thématiques dans l'ergonomie du site avec un filtrage des mots-clés par thématique (on clique une thématique et le champs des mots-clés accessibles se réduit)

Thématiques existantes :
  -  Arts et lettres
  -  Histoire
  -  Monde numérique
  -  Philosophie
  -  Politique et société (comprend les chroniques et donc l'actualité)
  -  Sciences et environnement
