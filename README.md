# LADISPE
## Politecnico di Torino

![PoliTO logo](https://upload.wikimedia.org/wikipedia/it/4/47/Logo_PoliTo_dal_2021_blu.png)

**LADISPE** is a lab inside of **Politecnico di Torino** which is the engineering university of Turin.

This web application is addressed to provide some information about the lab and some functionalities for the managing of news, posts and of the courses of which the exercise sessions take place in the lab. 


## App architecture

### Frontend
The frontend of this application is coded in Vue 3.
Vuetify 3 (beta) has been used for the UI.

### Backend

The backend is provided by a Django application served by Gunicorn web server.

Some libraries from *pip* has been used (see *requierments.txt*), particularly a custom patch has been applied to Django Filebrowser, in order to provide a private folder for each user registered to the site.

Some basics functionalities for the LDAP authentication have been introduced, in order to allow the users to authenticate with the university credentials.

Django admin is used to manage the application models.

### Docker
Docker has been used to build the production image.
Particularly there are three Docker containers which serve the application.

Nginx container has been chosen to handle static files and to provide the proxy functionalities to connect to Gunicorn.
The frontend is built with a Node image before Nginx has been deployed.

The backend is also a multistage build, because it is built with a Python image and enventually served with an another Python container.

Postgres has been chosen as database.


## Development

### Frontend
During the development, the frontend has to be served as a standard Node application.
In order to run in debugging mode it is required that the enviroment files are present in the frontend directory *(read the Enviroment variables section of this README)* and that in the same folder the following command has been executed:
```
NODE_ENV=dev DEBUG=* npm run serve
```
If VSCode is used, when the application is ready it is possible to run the frontend configuration  of the lauch.json to start the debugging.

### Backend
It is possible to run the backend configuration of the launch.json in VSCode in order to debug the Django application.
See the *Enviroment variables* section of this README to understend how manage the enviroment.


## Django admin
Django admin can be used to add, delete or modify the entities of the application.
By default a *staff user* can have access to the admin page, but he cannot add or modify any content.
In order to grant permissions, Django groups policies have to be used.

Two special groups are present: *Borsisti* and *Professors*.
The first should be used to manage the student staff, the second to manage the professors.
They are not created on the app initialization, therefore thay have to be manually created.

Also to give access to the Filebrowser, a group policy has to be set.

A special exception exists for the *Home* gallery, which allows modifications only by a *superuser* .

In the development version of the application a default user is created: *admin@test.org* with password *ladispe* .


## Enviroment variables
Some .env files have been provided tu run this project.
The variables in the latter files are not sensible information.
Other secret or local variables are needed for the application, these can be provided with .env.local file during the development.

The local enviroment variables files have to be placed in the location specified in the launch.json and in the docker-compose file.

The enviroment variables for the Vue application are used only during the compiling phase; during the production phase, the application will automatically use *window.location.origin* as base url.
During the debugging phase if one wants to overwrite the base_url setting, he can do it placing a .env.local file in the frontend folder.

During the production phase the enviroment variables not present in the repository, have to be specified as Docker container enviroment variables.

### Frontend

#### Project variables
- VUE_APP_API_ENTRYPOINT: prefix for the API url (the default is hardcoded in the Django urls settings) (default: api/)
- VUE_APP_MEDIA_URL_PREFIX: prefix for the media files url (default: storage/)

#### Local variables
- VUE_APP_URL: backend's base url (not required for the production phase) (example: http://127.0.0.1:8000)


### Backend
Keep the DB variables coherent with the Postgres variables and the URL variables coherent with the frontend variables.

#### Project variables
- DEBUG: Django debug mode (default: off)
- CORS_ALLOW_ALL_ORIGINS: cross-origin resource sharing allow all domains (see [django-cors-headers DOC](https://pypi.org/project/django-cors-headers/)) (default: off)
- MEDIA_URL: prefix for the media files url (default: storage/)
- MEDIA_ROOT: path (in the Docker container) of the root folder for the media files (default: /home/app/mediafiles/)
- STATIC_ROOT: path (in the Docker container) of the root folder for the static files of Django (default: /home/app/staticfiles/)
- SQLITE_ON: decide if use or not SQLite, off course in production this has to be off (default: off)
- SQL_ENGINE: Django database engine (default: django.db.backends.postgresql)
- SQL_DATABASE: he name of the database used by the backend (default: ladispe)
- SQL_HOST: the hostname of the database (default: db)
- SQL_PORT: the port of the database (default: 5432)

#### Local variables
- ALLOWED_HOSTS: allowed server names (see [Django DOC](https://docs.djangoproject.com/en/4.0/ref/settings/)) (example: localhost,127.0.0.1)
- CSRF_TRUSTED_ORIGINS: allowed origing url to avoid cross-site request forgery attack (see [Django DOC](https://docs.djangoproject.com/en/4.0/ref/settings/)) (example: https://localhost:4443,http://localhost:8888,https://127.0.0.1:4443,http://127.0.0.1:8888)
- SECRET_KEY: Django secret key (choose a long and randomic one) (example: this-is-not-a-good-secret)
- SQL_USER: the username used for the database (example: ladispe)
- SQL_PASSWORD: the password used for the database (example: ladispe)
- LDAP_AUTH: decide if use or not the LDAP authentication (not stable yet) (default: off)
- AUTH_LDAP_BIND_DN: domain name for the LDAP binding (example: ADMIN\siteadmin)
- AUTH_LDAP_BIND_PASSWORD: password for the LDAP binding
(example: mypassword)
- AUTH_LDAP_SERVER_URI: server uri of the LDAP server (example: ldap://dc01.mydomain.com)
- SEARCH_STRING: the string used to query the LDAP server (example: dc=mydomain,dc=com)

### Nginx

#### Project variables
- SSL_DIRECTORY: the directory in which the SSL key and certificate are present (default: /etc/ssl/ladispe/) (if using Docker secrets, default: /run/secrets/)
- SERVER_TOKENS: Nginx server tokens (default: off)

#### Local variables
- CLIENT_MAX_BODY_SIZE: Nginx max size of the client request (increase this value to allow bigger files to be upploaded) (example: 100M)
- SERVER_NAME: Nginx server name (example: localhost)


### Postgres
Keep this variables coherent with the Django variables.

#### Project variables
- POSTGRES_DB: the name of the database used by the backend (default: ladispe)

#### Local variables
- POSTGRES_USER: the username used for the database (example: ladispe)
- POSTGRES_PASSWORD: the password used for the database (example: ladispe)


## API
The backend is made by three Django applications: LADIContent, LADICourses and LADIUsers.
All the API requests use the GET method, because they are statelessness (modifications are allowed with Django admin).

All the API url are in the format */api/name_of_model/* for the fetching and */api/name_of_model/count/* to count the entities.

There are some common parameters for LADIContent and for LADICourses used to fetch from the database:
- attributes: list of boolean attributes different for every model, if present in the GET request, they required to be true) (eg. &attributes=public,light)
- id: used to get a specific object from the database (using its numeric id)
- keyword: used for the WHERE clause (* for all the objects)
- limit: max number of entries returned
- offset: offset for the entries returned (usefull when there are many pages in the frontend to see the results)
- order: column used to order the result
- sort: order of the result (*asc* for ascendent order, *desc* for descendent order)

### LADIContent
LADIContent is addressed to manage all the content of the site, despite the courses and the lectures.

See the Django admin section of this README to understend how to work with the *Home* gallery.
- api/ladiforms/
- api/ladiforms/count/
- api/ladigalleries/
- api/ladigalleries/count/
- api/ladigalleries/pictures/ : get the all the pictures of a specific gallery
- api/ladinews/ : *in_evidence* flag is used to get in evidence news
- api/ladinews/count/
- api/ladipictures/
- api/ladipictures/count/
- api/ladistaffs/
- api/ladistaffs/count/
- api/ladistories/
- api/ladistories/count/

### LADICourses
LADICourses is addressed to manage the courses and the lectures.
Not all the API requests are managed by the database functions, therefore it is not guaranteed that all the GET parameters work with all the requests.
- api/ladicourses/ : only superusers can see not public courses (*public* flag)
- api/ladicourses/count/
- api/ladicourses/lectures/ : get the all the lectures of a specific course
- api/ladicourses/materials/ : get the materials of a specific course, this is not a database API, therefore only *id* is accepted as parameters and it is used to specify the id of the course of which the materials are required
- api/ladilectures/
- api/ladilectures/count/

### LADIUsers
LADIUsers is addressed to provide information about the users of the application.
Only superusers can fetch information regarding other users than theirself, but there is an exception: when a user is also LADIStaff, his information are public.
- api/ladiuser/ : only *id* is accepted as parameters and it is used to specify the id of the user of who the information are required