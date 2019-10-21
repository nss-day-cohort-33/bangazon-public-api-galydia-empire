# python-bangazon-api-template
# Installations and Configuration for a DRF Project

## Creating the Project

```sh
cd ~/workspace/python
django-admin startproject bangazon
```

## Virtual Environment

A virtual environment allows you to install packages in the scope of this project without polluting global, system package installations.

```sh
cd bangazon
python -m venv bangazonapiEnv
source ./bangazonapiEnv/bin/activate
```

Once the virtual environment is activated, you may notice that you prompt in the terminal change to have the word `bangazonEnv` either in parenthesis or has the word `via` before it.

## Installed Required Packages

Now you use pip to install all of the packages needed for this project.

```sh
pip install django autopep8 pylint djangorestframework django-cors-headers pylint-django
```

Once they are installed, you use the `freeze` command to capture all of the packages, and their version numbers, in a file so that other developers can easily install those requirements on their machine.

```sh
pip freeze > requirements.txt
```

## Allowing Common Variables Names

The pylint package is very good at ensuring that you follow the community standards for variable naming, but there are certain times that you want to use variable names that are short and don't use snake case. You can put those variable names in a `.pylintrc` file in your project.

Without this configuration, your editor will put orange squiggles under those variable names to alert you that you violated community standards. It becomes annoying, so you override the default rules.

```sh
echo '[FORMAT]
good-names=i,j,ex,pk
' > .pylintrc
```

In Visual Studio Code, `cmd+shift+p` and open "Preferences: Open Settings (JSON)". Add the following configuration item to the object.

```json
"python.linting.pylintArgs": [
    "--load-plugins=pylint_django"
],
```

## Create Base Django Tables

You may remember that Django gives you user and role management tables out of the box, and there is a built-in migration file that makes the tables for you. Go ahead and run that migration to set up the initial Django tables.

```sh
python manage.py migrate
```

## API Application

Now that the project is set up and has some initial configuration, it's time to create your application for the API you are building.

```sh
python manage.py startapp bangazonapi
```

Now you need to update your application settings to enable Django REST Framework, CORS headers, and your application. Replace the following sections, and add the sections marked as new, in your `settings.py` file with the code below.

> ##### `settings.py`

```sh
# Replace existing list
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'bangazonapi',
]

# This is new
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10
}

# Replace existing list
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# This is new
CORS_ORIGIN_WHITELIST = (
    'http://localhost:3000',
    'http://127.0.0.1:3000'
)
```

## Basic Setup of Routing

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
```

## First Run

Now you can start the project and verify that everything was configured correctly.

```sh
python manage.py runserver
```

Then open the URL of `http://127.0.0.1:8000/` in your browser and you should see a web page with no errors on it. If you do see error, please visit the instruction team.

## Updating Database with Migration

The models are set up, it's time to use them to create your tables in the database. The first step is to import all the models into the `urls.py` module. Add the following import statement.

> ##### `bangazonapi/urls.py`

```py
from bangazonapi.models import *
```

Then create a migration in the terminal.

```py
python manage.py makemigrations bangazonapi
```

Once the migration is created, you run it to create the tables.

```py
python manage.py migrate