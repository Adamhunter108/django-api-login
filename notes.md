# Notes: 📝
## Build an API with authenication functionality

### Project Set Up
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

### Start Django App
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

now add a route that points to the app in the root `urls.py`
```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('<app-name>.urls')),

]

```

---
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

create `<app-name>/urls.py`

in `<app-name>/urls.py`, include routes for Simple JWT’s TokenObtainPairView (and TokenRefreshView) views:
```python
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    ...
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    ...
]

# note: can change the url paths to something like 
path('users/login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
```

point root `urls.py` to app-name.urls:
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]
```


Customize Token in `settings.py`:
```python

# Customize the JWT Token:
# https://django-rest-framework-simplejwt.readthedocs.io/en/latest/settings.html
from datetime import timedelta

SIMPLE_JWT = {
    # 'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'ACCESS_TOKEN_LIFETIME': timedelta(days=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    # 'SIGNING_KEY': settings.SECRET_KEY, # this was throwing an error
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

```

in app/`views.py`:
```python
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['name'] = user.name
        # ...

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# or custimize 
```


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
from rest_framework_simplejwt.tokens import RefreshToken

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

# extending off UserSerializer
class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'name', 'isAdmin', 'token']

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)

    # generating (serializing) a user, take that user object and return back another token with the initial response
```

and now the actual views:
```python
from django.shortcuts import render
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserSerializer, UserSerializerWithToken

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    # @classmethod
    # def get_token(cls, user):
    #     token = super().get_token(user)

    #     # Add custom claims
    #     token['username'] = user.username
    #     token['message'] = 'why is the sky blue?  why is water wet?'

    #     return token

    # commented out function above puts the username and a message encrypted into the access token
    # below function serializes data and makes it accessible in the API, making it easier to grab from the frontend

    def validate(self, attrs):
        data = super().validate(attrs)
        # data['username'] = self.user.username
        # data['email'] = self.user.email

        # changing to for loop to output the data from the serializer instead of adding manually
        serializer = UserSerializerWithToken(self.user).data
        for key, value in serializer.items():
            data[key] = value

        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

```

---

### Set up CORS Headers
You need to allow outside sources to connect to the API, like Postman.
[Django CORS](https://github.com/adamchainz/django-cors-headers)
```bash
$ # install library
$ pip install django-cors-headers
$ # update dependencies txt
$ pip freeze > requirements.txt
```
In `settings.py`, add to INSTALLED_APPS, the middleware, and CORS_ALLOWED_ORIGINS

---

### Log in user
now at `http://localhost:8000/api/users/login/` (or whatever url path), My Token Obtain Pair view can log a user in and return JWT and other specified info.  

this also means sending data to `http://localhost:8000/api/users/login/` from a frontend or API testing tool like Postman, you can get your token and log in.

```json
{
    "username": "<your-name>",
    "password": "<your-pass>"
}
```

---

### Register a user

in `views.py`:
```python
@api_view(['POST'])
def registerUser(request):
    data = request.data
    # print(data)
    
    try:
        user = User.objects.create(
            first_name=data['name'],
            username=data['email'],
            email=data['email'],
            password=make_password(data['password'])
        )
        serializer = UserSerializerWithToken(user, many=False)
        return Response(serializer.data)
    except:
        message = {'detail':'That email is already registered with us.'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)
```

then in `urls.py`:
```python
from django.urls import path
from . import views

urlpatterns = [
    path('users/login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/register/', views.registerUser, name='register'),
]
```

now at `http://localhost:8000/api/users/register/` you can register a new user by sending name, email and password:
```json
{
    "name": "snoopy",
    "email": "snoopy@aol.com",
    "password": "woodstock"
}
```

---
### Get logged in users data
send Bearer token from login to `http://localhost:8000/api/users/profile/` to get user's data.
```python
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    user = request.user
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)
```
---
### Get all users (if admin)
if token is from an admin user, you can send Bearer token to `http://localhost:8000/api/users/` to get a list of registered users
```python
@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUsers(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)
```