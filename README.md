# Project 1

Web Programming with Python and JavaScript

This repo contains the files required for a website that allows a user to search for books and leave reviews.
import.py allows books.csv to be uploaded as a sql database hosted by heroku.
application.py contains flask app.routes for a locally hosted website where users can register, login, search for books, leave reviews and when querying the /api/<some-isbn> route, will query the goodreads API and return a json with goodreads data.
 