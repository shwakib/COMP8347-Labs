# Development Guide

1. check if there's a `.venv` folder exists or not
   1. create using `python -m venv ./.venv`
   2. activate the virtual environment using:
      1. linux/mac : `source .venv/bin/activate`
      2. windows (cmd): `.venv\Scripts\activate.bat`
2. dependencies: 
   1. install when switch to a new env or at first `pip install -r requirements.txt`
   2. if you install any package then `pip freeze > requirements.txt` to all the dependency to the `requirements.txt`
3. migrations:
   1. after every pull: `python manage.py migrate` > this will change your db according to the `models.py`
   2. if you want to do some change to your DB schema (`models.py`) then
      1. <span style="color:red">discuss with us first</span>
      2. change the schema
      3. `python manage.py makemigrations` > create new migration files based on the changes
      4. `python manage.py migrate` > apply these migrations to the database
4. Development:
   1. Please use pyCharm for development; It will be easier to debug
5. RUN:
   1. IDE (pyCharm):
      1. TBA
   2. terminal:
      1. with 8000 as port: `python manage.py runserver`
      2. with custom port:  `python3 manage.py runserver 8080`
