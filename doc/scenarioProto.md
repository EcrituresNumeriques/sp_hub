# Scénario prototype

**Objectif** : produire une preuve de concept articulant trois types d'objets :

1. des articles scientifiques
2. des conversations
3. des annotations

## Articles
Les articles scientifiques sont stockés dans une base XML au format HTML et seront requêtés via API RESTXQ.

## Annotations
Les annotations sont des instances d'annotations Hypothes.is et sont de deux types :

1. annotation de page
2. annotation intra-textuelle (fragment d'article)

Chaque annotation est caractérisée par :

* un objet référence (page ou fragment de texte à l'intérieur d'une page)
* un auteur
* un commentaire formaté (md)
* des mots-clés

## Conversations

Chaque conversation est caractérisée par :

* un titre
* des mots-clés
* des fils de discussions (annotations de page attachées à la page de la conversation)
* des ressources agrégées :
  * articles
  * annotations d'articles (intra-textuelles)

L'agrégation se fait sur la base des mots-clés selon un algorithme à concevoir.

## Gestion utilisateur

Hors-POC mais à anticiper :

Il est prévu que la plateforme (hub) fasse une gestion fine des utilisateurs, en distinguant :
* les administrateurs
* les éditeurs  : peuvent créer des articles (import de document HTML dans la base BASEX) et des conversations (avec paramétrage des algorithmes d'agrégation)
* les auteurs   : ont un statut particulier et une page auteur dédiée
* les lecteurs  : peuvent créer des annotations.

Il sera nécessaire de maintenir pour chaque utilisateur une liste de ses annotations (et autres activités à définir)

Pour la preuve de concept, le backoffice éditeur n'est pas à développer.

## Ressources pour la POC

### Articles

id   | titre | auteur | mots-clés
:--  | :--   |  :--   | :--
SP1244 | Progressistes  | Niels Planel  | progressisme ; mouvement conservateur ; cosmopolitisme ; économie ; mondialisation ; nationalisme
SP1245 | Building Global Community | Gérard Wormser | Facebook, éditorialisation, algorithmes, connectivité, public, médias, globalisation, opinion, bulle de filtre, segmentation
SP1246 | Picsou: quelques remarques sur la cupdité | Joëlle Zask | libéralisme, capitalisme, cupidité, passion, argent, théorie économique, Picsou
SP1249 | Il ne suffit que de regarder | William Delisle | Images, regard, éthique, objet-regard, Georges Didi-Huberman, psychanalyse, philosophie, Jacques Lacan, Sigmund Freud, Auschwitz, photographie
SP1250 | La Grande Transformation | Gérard Wormser | France, élection présidentielle, Front national, Macron, désaffiliation
SP1254 | Engagement radical, extrême ou violent | Caroline Guibet Lafaye | Engagement, radicalisation, alternation, illusion rétrospective, extrême gauche, Action Directe

### Conversation

* Titre : Ni gauche, ni droite
* Mots-clés : mondialisation, globalisation, capitalisme, radicalisation, extrême gauche, mouvement conservateur
