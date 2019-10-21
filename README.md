## Basic Setup of Routing
Replace the contents of bangazonapi/urls.py with the following code. You will configure the routes for your application in the next chapter after you set up your first view.
py
from django.conf.urls import url, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

router = routers.DefaultRouter(trailing_slash=False)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-token-auth/', obtain_auth_token),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
## First Run
Now you can start the project and verify that everything was configured correctly.
```sh
python manage.py runserver
Then open the URL of http://127.0.0.1:8000/ in your browser and you should see a web page with no errors on it. If you do see error, please visit the instruction team.
## Updating Database with Migration
The models are set up, it's time to use them to create your tables in the database. The first step is to import all the models into the urls.py module. Add the following import statement.
##### bangazonapi/urls.py
```py
from bangazonapi.models import *
Then create a migration in the terminal.
```py
python manage.py makemigrations bangazonapi
Once the migration is created, you run it to create the tables.
```py
python manage.py migrate## Basic Setup of Routing

Replace the contents of `bangazonapi/urls.py` with the following code. You will configure the routes for your application in the next chapter after you set up your first view.

```py
from django.conf.urls import url, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

router = routers.DefaultRouter(trailing_slash=False)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-token-auth/', obtain_auth_token),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
## First Run
Now you can start the project and verify that everything was configured correctly.
```sh
python manage.py runserver
Then open the URL of http://127.0.0.1:8000/ in your browser and you should see a web page with no errors on it. If you do see error, please visit the instruction team.
## Updating Database with Migration
The models are set up, it's time to use them to create your tables in the database. The first step is to import all the models into the urls.py module. Add the following import statement.
##### bangazonapi/urls.py
```py
from bangazonapi.models import *
Then create a migration in the terminal.
```py
python manage.py makemigrations bangazonapi
Once the migration is created, you run it to create the tables.
```py
python manage.py migrate
