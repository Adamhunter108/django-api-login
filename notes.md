# Notes: 📝
## Build an API with authenication functionality

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
Login to admin at `http://localhost:8000/admin`