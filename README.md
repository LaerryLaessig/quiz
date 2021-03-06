# Editable Quiz

Quiz with a editor to update, delete and create questions.

## environment variables
- USER_ADMIN
    - change in start.sh or in environment variable
    - default value admin
- PWD_ADMIN 
    - change in start.sh or in environment variable
    - default value admin
- SECRET_KEY
    - change in start.sh or in environment variable
    - default value secret_key

## UI-Endpoints
### '/'
The quiz.
### '/admin
Quiz editor with authentication.

## dependencies
 - flask
    - micro web framework
    - https://palletsprojects.com/p/flask/
 - flask_httpauth
    - extension that simplifies the use of HTTP authentication with Flask routes
    - https://flask-httpauth.readthedocs.io/en/latest/
 - flask_sqlalchemy
    - extension that simplifies using SQLAlchemy
    - https://flask-sqlalchemy.palletsprojects.com/
- flask_bootstrap
    - extension that simplifies using bootstrap4
    - https://github.com/mbr/flask-bootstrap
 - waitress
    - Waitress is meant to be a production-quality pure-Python WSGI server with very acceptable performance
    - https://github.com/Pylons/waitress

