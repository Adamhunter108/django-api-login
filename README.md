# django-api-login
<img src="https://cdn.worldvectorlogo.com/logos/django.svg" width="50" height="50"/>

### `About:`
A RESTful API for managing user accounts for Django apps.

The API features JWT (JSON Web Token) authentication, and full CRUD (Create, Read, Update, Delete) functionality for user accounts.  

### `API URL Paths:`

Register an account:
```
http://localhost:8000/api/users/register
```

Log into an account:
```
http://localhost:8000/api/users/login
```

Get logged in user's data:
```
http://localhost:8000/api/users/profile
```

Get all app users' data (admin only):
```
http://localhost:8000/api/users/
```

Get a specific user's data (admin only):
```
http://localhost:8000/api/users/{id}
```

Update logged in user's data:
```
http://localhost:8000/api/users/update/{id}
```

Delete a user's account:
```
http://localhost:8000/api/users/delete/{id}
```


### `Run Locally:`
---
#### `Requirements:`
* Python 3   <img src="https://cdn.worldvectorlogo.com/logos/python-5.svg" width="25" height="25"/>
---

```bash
$ # change into backend directory
$ cd backend
$ # create virtual environment
$ virtualenv venv
$ # activate venv
$ . venv/bin/activate # for mac/linux
$ # install dependencies
$ pip install -r requirements.txt
$ # migrate admin and auth to SQLite db
$ python manage.py migrate
$ # create superuser so you can login to /admin
$ python manage.py createsuperuser
$ # follow prompts
$ # start django server
$ python manage.py runserver
```
Unless specified otherwise, the API will be available at port: 8000 