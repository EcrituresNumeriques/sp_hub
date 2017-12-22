### (#E1) En tant qu'éditeur, je veux pouvoir éditer les mot-clés

Pour un mot-clé éditeur :

* modification des champs (pour une v2, interrogation du [webservice isidore](http://rd.rechercheisidore.fr/ondemand/) pour la suggestion à la volée d'identifiant Rameau et autres autorités. Voir les développements sur [chaineEditorialeSP](https://github.com/EcrituresNumeriques/chaineEditorialeSP/))
* si FR, ajout d'une traduction : l'autocomplétion (avec présentation de langue) amène à :
 	1. l'association à un mot-clé existant ou
	2. la création d'un nouveau (une création de mot-clé éditeur nécessite un identifiant sur une autorité)
	- Exemple: je veux ajouter une traduction à "Monde numérique", je tape `digit` et l'autocomplétion suggère `digit-al world (en)` s'il existe.

Pour un mot-clé auteur :
* modification des champs
* si FR, ajout d'une traduction dans une autre langue : même principe que mot-clé éditeur, mais l'autorité n'est pas nécessaire.
* si autre langue, l'ajout d'une traduction sera nécessairement en français : l'autocomplétion ne se fait que parmi les mots-clés auteurs FR.
