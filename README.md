#Editable Quiz

Answers will checked with Event-Sourcing.

##environment variables
- USER_ADMIN
    - change in start.sh or in environment variable
- PWD_ADMIN 
    - change in start.sh or in environment variable

##UI-Endpoints
###'/'
The quiz.
###'/admin
Quiz editor with authentication.

 ###Libaries
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
 - wordcloud
   - Wordcloud generator
   - https://github.com/amueller/word_cloud