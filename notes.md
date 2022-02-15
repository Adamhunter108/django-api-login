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