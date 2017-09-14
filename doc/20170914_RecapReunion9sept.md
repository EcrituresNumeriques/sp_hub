# Récap
de la réunion [[chaire_admin/SensPublic/20170911_RéunionRentrée.md]]

## Mots-clés

Soit l'organisation des mots-clés suivantes :

1. mots-clés éditoriaux : ils sont alignés sur Rameau et son organisés selon la même taxonomie que sous SPIP :
  * Lieux
  * Auteurs/personnes
  * Sujets
  * Domaine artistique
  * Thématiques (voir ci-dessous)
2. mots-clés auteurs: ils ne sont pas alignés. Ils sont associés à l'objet auteur.
3. mots-clés utilisateurs : ils ne sont pas alignés. Il faut conserver l'information : **qui** a utilisé **quel** mot-clé, **où** et **quand** (comme sur hypothes.is)

Question technique : comment exprimer cette taxonomie de mot-clé dans les html ? On s'oriente vers des balises RDF-a. Suggestions bienvenues.

Les mots-clés auteurs et utilisateurs sont pratiquement les mêmes objets. Ce qui les distingue c'est qui les crée, donc potentiellement, aucune distinction.

Les mots-clés auteurs et utilisateurs peuvent être considérés comme des mots-clés _candidats_ pour "remonter" dans les mots-clés éditoriaux alignés. C'est une négociation entre top-down et bottom-up. Décision qui revient aux éditeurs et suppose un travail de veille sur les mots-clés émergents.

Il faut prévoir : de donner des outils aux éditeurs pour mener cette négociation :
  * identifier des mots-clés potentiels (candidats) : cluster, visualisation, etc.
  * trouver des aligements et les choisir (requête isidore)
  * créer de nouveaux mots-clés alignés dans la base.

Il faut donc prévoir et choisir : 1. soit qu'un mot-clé (et son historique) puisse changer de statut ou d'objet. 2. Soit on fait une rupture nette et les mots-clés éditoriaux nouveaux vont cohabiter avec des mots-clés utilisateurs anciens. Risque de doublon lors d'une recherche.

Lors de la production de l'archive html, les mots-clés auteurs seront récupérés automatiquement et/ou manuellement quand il y en a et réinsérés dans l'archive html en tant que tel.

Exploitation : sur SP hub, les champs de recherche et champs de tagging présenteront en autocomplétion tout confondus les 3 types de mots-clés : pas de hiérarchisation, mais potentiellement une distinction (couleur, picto alignement, à définir)

## Thématiques

Dans Spip, les articles étaient scindés en 6 thématiques présentant les champs d'étude de la revue. Les thématiques demeurent mais comme des champs sémantique de mot-clés davantage que comme 6 mots-clés fermes. Les thématiques sont donc plus souples, non-excusive.

Dans un premier temps, on conserve la donnée thématique comme un mot-clé dans les archives html.
Pour un chantier futur, on pourra considérer que les mots-clés d'un article définissent sa thématique par proximité au champs sémantique de chaque thématique.

Exploitation: on implémente les thématiques dans l'ergonomie du site avec un filtrage des mots-clés par thématique (on clique une thématique et le champs des mots-clés accessibles se réduit)

thématiques existantes :
  -  Arts et lettres
  -  Histoire
  -  Monde numérique
  -  Philosophie
  -  Politique et société (comprend les chroniques et donc l'actualité)
  -  Sciences et environnement

## Dossiers & Actes

Il y a dans Spip plusieurs types de contenus, dont deux particuliers :

* Dossier (rubrique 109): qui comprend un article-sommaire et une liste d'articles
* Actes de colloque (rubrique 107): qui comprend un article-sommaire et une liste d'article

Les dossiers et actes de Spip deviendront des conversations dans SPHub, soit une agrégation "moins éditoriale" de contenus comprenant les articles originaux du dossier + tout fragment ou objet pertinent.

## Conversations

Principes éditoriaux :
* une conversation n'est pas une agrégation strictement algorithmique. C'est l'éditeur qui assure une certaine cohérence des contenus et fragments qui s'agrègeront dans la conversation. Il n'y a donc pas d'algorithme d'agrégation alimentant continuellement les conversations.
* Par contre, une interface éditeur doit permettre au directeur de conversation (équivalent du directeur de dossier) de simplement requêter et sélectionner des contenus/fragments à ajouter à la conversation. Les algorithmes de requêtage produisent des résultats qui sont des suggestions de ressources.
* Principe directeur : faire cohabiter la temporalité de la conversation avec la spatialité des ressources. Design à faire.
* Un des objectifs possible de la conversation est la production de textes (articles) qui viendront clôturer la conversation avant qu'elle ne soit archivée (accessible en lecture seule). La conversation sert alors à fixer des orientations, discuter des problématiques, débattre, et converger vers une stabilisation.

## Cycle de vie et archive

### Article

Nécessaire de versionner plusieurs états d'un article et notamment :

* à date de publication sur SPHub : archive html initiale
* à date de dépôt chez Erudit : archive html + xml Erudit enrichie des appropriations de la communauté : annotations, tagging, etc.
* à discrétion de l'éditeur lorsque l'article fait l'objet d'une attention particulière : archive html enrichie

Le principe est donc bien de réintégrer les éléments de la conversation dans le html, ou en tout cas dans une version (xml?) hors de la base de donnée de la plateforme SPHub.

aspect technique :
  * le cas des mots-clés : on peut imaginer qu'ils s'ajoutent dans le document html comme métadonnées du html.
  * le cas des annotations : comment sont ils intégrés ? insertion d'ancres/id dans le corps du html et adjonction d'un fichier xml contenant les annotations?
  * penser à une métadonnées "version" (voir DubliCore)

### Conversation

Quelle archivage de la conversation est pertinente ?
  * Snapshots HTML (type wget) successifs d'une conversation ?
  * Dump statiques (json?) des diff. base de donnée pour être capable de ré-éditorialiser une conversation ?
