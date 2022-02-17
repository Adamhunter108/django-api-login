# django-api-login
<img src="https://cdn.worldvectorlogo.com/logos/django.svg" width="50" height="50"/>

### `About:`
A RESTful API for managing user accounts for Django apps.

The API features JWT (JSON Web Token) authentication, and full CRUD (Create, Read, Update, Delete) functionality for user accounts.  

### `API URL Paths:`

#### Register an account:
```json
{URL}/api/users/register
```

#### Log into an account:
```json
{URL}/api/users/login
```

#### Get logged in user's data:
```json
{URL}/api/users/profile
```

#### Get all app users' data (admin only):
```json
{URL}/api/users/
```

#### Get a specific user's data (admin only):
```json
{URL}/api/users/{id}
```

#### Update logged in user's data:
```json
{URL}/api/users/update/{id}
```

#### Delete a user's account:
```json
{URL}/api/users/delete/{id}
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
$ # if no port specified, django serves at port 8000$ 
```
>note: you may specify a port as an argument on the last command, if no port specified, django serves at port 8000 (or `http://127.0.0.1:8000/` or `http://localhost:8000/`)