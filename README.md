# SP Hub

Pour démarrer l'application:
* installer pip: easy_install pip
* installer virtualenv: easy_install virtualenv virtualenvwrapper
* créer un virtualenv, par exemple: virtual ~/.virtualenvs/django
* se mettre dans ce virtualenv: source ~/.virtualenvs/django/bin/activate
* le prompt shell doit afficher (django) au début
* installer les dépendances: pip install django django-bootstrap3 requests httplib2 urllib3
* git clone
* cd sp_hub
* créer le schéma de base: ./manage.py migrate
* créer un superuser: ./manage.py createsuperuser
* ./manage.py runserver
* accéder au serveur sur http://127.0.0.1:8000/
* on peut login sur http://127.0.0.1:8000/admin/ (interface d'admin de base de Django)
