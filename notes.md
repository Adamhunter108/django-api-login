# Notes: 📝
## Build an API with authenication functionality

#### Project Set Up
```bash
$ # create virtual environment
$ virtualenv venv
$ # activate venv
$ . venv/bin/activate
$ # if using existing project, install dependencies
$ pip install -r requirements.txt
$ # if new project:    
$ # install django
$ python -m pip install django
$ # create django project
$ django-admin startproject <project-name>
$ # change into project
$ cd <project-name>
$ # migrate admin and auth to SQLite db
$ python manage.py migrate
$ # create superuser so you can login to /admin
$ python manage.py createsuperuser
$ # follow prompts
$ # start django server
$ python manage.py runserver
```


Now go to `http://127.0.0.1:8000/` or `http://localhost:8000/` in a browser to see if everything is kosher so far. You should see a little 🚀 success message.

Login to admin at `http://localhost:8000/admin`.

#### install Django REST Framework
```bash
$ # install django REST framework
$ pip install djangorestframework 
$ # DRF docs suggest the next two dependencies
$ # Markdown support for the browsable API.
$ pip install markdown
$ # Filtering support
$ pip install django-filter  
```

Add `'rest_framework', `to `INSTALLED_APPS` in `project-name/settings.py`
```python
INSTALLED_APPS = [
    ...
    'rest_framework',
]
```

If you're intending to use the browsable API you'll probably also want to add REST framework's login and logout views. Add the following to your root `urls.py` file. (note: path can be anything)
```python
from django.urls import path, include
# throw on that include

urlpatterns = [
    ...
    path('api-auth/', include('rest_framework.urls'))
]
```

Now we need a django app inside of the project.
```bash
$ python manage.py startapp <app-name>
```
Add app to `INSTALLED_APPS` in `project-name/settings.py`
```python
INSTALLED_APPS = [
    ...
    'rest_framework',
    'app-name',
]
```

### Authentication:
[DRF Token Authentication](https://www.django-rest-framework.org/api-guide/authentication/#tokenauthentication)
Authenticate through DRF API using token authentication: 
JSON Web Token is a fairly new standard which can be used for token-based authentication. Unlike the built-in TokenAuthentication scheme, JWT Authentication doesn't need to use a database to validate a token. A package for JWT authentication is `djangorestframework-simplejwt` which provides some features as well as a pluggable token blacklist app.

[Django REST Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)
```bash
pip install djangorestframework-simplejwt
```

in `settings.py`, add rest_framework_simplejwt.authentication.JWTAuthentication to the list of authentication classes:
```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

```

---

```bash
$ pip freeze > requirements.txt
```

Now we need some serializers.  Serializers allow complex data such as querysets and model instances to be converted to native Python datatypes that can then be easily rendered into JSON, XML or other content types.

Add the file `project-name/app-name/serializers.py`

Django comes with a User model [docs](https://docs.djangoproject.com/en/4.0/ref/contrib/auth/)

[DRF ModelSerializer](https://www.django-rest-framework.org/api-guide/serializers/#modelserializer)

Import the django user model and serializers from DRF in  `serializers.py`.  Then create a serializer class that extends off DRF ModselSerializer.
```python
from django.contrib.auth.models import  User
from rest_framework import  serializers

class  UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    id = serializers.SerializerMethodField(read_only=True)
    isAdmin = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'name', 'isAdmin']

    # you can create serializer method fields that return back custom attributes

    def get_id(self, obj):
        return obj.id

    def get_isAdmin(self, obj):
        return obj.is_staff

    def get_name(self, obj):
        # passing into built in django field first_name
        name = obj.first_name
        if name == '':
            name = obj.email
        return name

```