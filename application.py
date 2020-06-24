import os
import psycopg2, requests, json
from tables import TableMake

from flask import Flask, session, render_template, request, redirect, url_for, jsonify, flash
from flask_session import Session
from sqlalchemy import create_engine, MetaData, Table, Column, String, select
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)
app.config["SECRET_KEY"] = "goodluck"

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

createReviews = ('CREATE TABLE IF NOT EXISTS "reviews" ('
    ' revid SERIAL PRIMARY KEY,'
    ' isbn VARCHAR REFERENCES books,'
    ' userid INTEGER REFERENCES users,'
    ' review VARCHAR,'
    ' rating INTEGER);')

db.execute (createReviews)
db.commit()

createUsers = ('CREATE TABLE IF NOT EXISTS "users" ('
    'username VARCHAR NOT NULL,'
    'password VARCHAR NOT NULL,'
    'userid SERIAL UNIQUE,'
    'PRIMARY KEY (userID));')

db.execute (createUsers)
db.commit()

@app.route("/home", methods = ["POST", "GET"])
@app.route("/", methods = ["POST", "GET"])

def index():
    if request.method == 'GET':
            if 'USER' in session:
                return redirect(url_for("search", name = session['NAME']))
            else:    
                headline = "Please try signing in or sign up"
                body = "Hello this is a body"
                return render_template ("index.html", headline=headline)

    if request.method == 'POST':
        usernamelog = request.form['usernamelog']
        passwordlog = request.form['passwordlog']

        if not usernamelog or not passwordlog:
            return render_template ("index.html", headline="Incorrect username or password")
    
        for i in usernamelog:
            if i == "'" or i.isspace():
                return render_template ("index.html", headline= "not a valid username")
    
        for i in passwordlog:
            if i == "'" or i.isspace():
                return render_template ("index.html", headline= "not a password")

        databaseQuery = db.execute('SELECT * FROM users WHERE (username = :usernamelog AND password = :passwordlog)',
        {"usernamelog": usernamelog, "passwordlog": passwordlog}).fetchone()

        if databaseQuery:
            session['USER'] = databaseQuery.userid
            session['NAME'] = databaseQuery.username.capitalize()
            return render_template ("search.html", name = session['NAME'])
        else:
            return render_template ("index.html", headline="Incorrect username or password")


@app.route('/signup')
def signup():

    return render_template ("signup.html")

@app.route("/signupcomplete", methods = ['POST', 'GET'])
def signupcomplete():

    if request.method == 'GET':
        return render_template("index.html")

    else:

        username = request.form['username']
        password = request.form['password']

        for i in username:
            if i == "'" or i.isspace():
                return redirect(url_for('signup', headline="Please use a valid username"))
        
        for i in password:
            if i == "'" or i.isspace():
                return redirect(url_for('signup', headline="Please use a valid password"))
            else:
                continue

        if username == "" or password == "":
            headline = "Please complete both fields"
            return render_template("signup.html", headline="Please use a valid password")
        
        elif db.execute("SELECT username FROM users WHERE username = :username", {"username": username}).rowcount != 0:
            headline = "This username is taken"
            return render_template("signup.html", headline=headline)

        else:

            db.execute ("INSERT INTO users (username, password) VALUES (:username, :password)",
            {"username": username, "password": password})
            db.commit()

            headline = "Signup Successful"
            return render_template("index.html", headline = headline)

@app.route("/logout")
def logout():
    if 'USER' in session:
        session.pop('USER',None)
        session.pop('NAME', None)

        return render_template("index.html", headline="logged out")

    else:
        return render_template("index.html", headline="You are already logged out")


@app.route("/search", methods = ['POST', 'GET'])
def search():
    if request.method == 'GET':
        #if logged in, returns the search page, otherwise takes user back to the main page
        if 'USER' in session:
            return render_template("search.html", name = session['NAME'])

        else:
            return render_template("index.html", headline="You have to login first to see the search page")

    #if post request submitted from a form being completed, attemps to convert all the form inputs into valid sqlAlchemy syntax
    #by adding a % to the end of the input (as SQL query is a LIKE query), if nothing was entered into the form, sets variable to ""
    #and correct sql statement is picked out.
    else:
        try:
            isbn = request.form['isbn'] + "%"
        except:
           isbn = ""
        try:
            title = request.form['title'].capitalize() + "%"
        except:
            title = ""
        try:
            author = request.form['author'] + "%"
        except:
            author = ""
        
    if isbn != "":
        books = db.execute("SELECT * FROM BOOKS WHERE (isbn LIKE :isbn)", {"isbn": isbn})

    elif title != "":
        books = db.execute("SELECT * FROM BOOKS WHERE (title LIKE :title)", {"title": title})
       
    else:
        books = db.execute("SELECT * FROM BOOKS WHERE (author LIKE :author)", {"author": author})

    if books.rowcount == 0:
        return render_template("search.html", headline = "No books found with those parameters") 
        
    else:
        return render_template("booksearchsuccess.html", books=books)


@app.route("/selectedbook/<string:isbn>", methods = ["GET", "POST"])
def selectedbook(isbn):
    apireq = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "qjfi7EyD90v3MlEghQNbBQ", "isbns": isbn})
    books = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn})
    reviews = db.execute("SELECT reviews.review, reviews.rating, users.username FROM reviews "
                        "INNER JOIN users ON reviews.userid = users.userid "
                        "WHERE isbn = :isbn", {"isbn": isbn})
    
    apiresult = apireq.json()
    
    rev_count =  apiresult['books'][0]['reviews_count']
    average_score = apiresult['books'][0]['average_rating']

    if request.method =="GET":     
        return render_template("selectedbook.html", books = books, reviews = reviews, rev_count = rev_count, average_score = average_score)

    else:
        rating = request.form['rating']
        rev = request.form['review']
        current = session["USER"]
       
        if db.execute ("SELECT * FROM reviews WHERE userid = :userid AND isbn = :isbn",
         {"userid": current, "isbn": isbn}).rowcount != 0:

            db.execute("UPDATE reviews SET review = :review, rating = :rating WHERE userid = :userid AND isbn = :isbn", 
            {"review": rev, "userid": current, "isbn": isbn, "rating": rating})
            db.commit()

            flash('Your review has been updated! Please refresh the page to see it displayed.')
            
            return render_template("selectedbook.html",  books = books, reviews = reviews, rev_count = rev_count, average_score = average_score)

        else:
            db.execute ("INSERT INTO reviews (isbn, userid, review, rating) VALUES (:isbn, :userid, :review, :rating)",
            {"isbn": isbn, "userid": current, "review": rev, "rating": 5})
            db.commit()
            flash('Your review has been submitted! It will be visible once you refresh the page')
            return render_template("selectedbook.html", books = books, reviews = reviews, rev_count = rev_count, average_score = average_score)

@app.route("/api/<string:isbn>")
def api(isbn):
    
    apireq = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "qjfi7EyD90v3MlEghQNbBQ", "isbns": isbn})

    if not apireq:
        return render_template("index.html", headline="404 book not found")

    else:
        dbreq = db.execute("SELECT * FROM books WHERE isbn = :isbn", {"isbn": isbn}).fetchone()
    
        apiresult = apireq.json()

        builtjson = {
    "title": dbreq.title,
    "author": dbreq.author,
    "year": dbreq.year,
    "isbn": dbreq.isbn,
    "review_count": apiresult['books'][0]['reviews_count'],
    "average_score": apiresult['books'][0]['average_rating']
    }

        return jsonify(builtjson)

        
            
    

    
