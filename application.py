import os
import psycopg2
from tables import TableMake

from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine, MetaData, Table, Column, String
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
#os.putenv("DATABASE_URL", "postgres://qhpnyexenogece:1c04bab21940e673a432d6354cc67440b4d2830e4213f84f18fddf392ff88b9e@ec2-52-202-22-140.compute-1.amazonaws.com:5432/d8tpvv7b4aadb")
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

#metadata = MetaData()
#users = Table('users', metadata,
#Column ('userID', Integer, primary_key=True),
#Column ('username', String(20), nullable=false),
#Column ('password', String(20), nullable=false)
#)

#users.create(engine, checkfirst=True)

#db.execute("IF (EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = 'dbo' AND TABLE_NAME = 'users'))
 #  
  # 
   #
   #BEGIN
    #  PRINT 'Database Table Exists'
   #END;
#ELSE
 #  BEGIN
  #    PRINT 'No Table in database'
   #END;  )


@app.route("/")
def index():
    headline = " Headline"
    body = "Hello this is a body"
    return render_template ("index.html", headline=headline)



@app.route('/signup')
def signup():
    
    #engine.execute ('CREATE TABLE IF NOT EXISTS "users" ('
     #  'username VARCHAR NOT NULL,'
      #  'password VARCHAR NOT NULL,'
       # 'userID VARCHAR NOT NULL,'
        #'PRIMARY KEY (userID));')

    command = ('CREATE TABLE IF NOT EXISTS "users" ('
       'username VARCHAR NOT NULL,'
       'password VARCHAR NOT NULL,'
        'userID SERIAL UNIQUE,'
        'PRIMARY KEY (userID));')

    db.execute (command)
    db.commit()

    #print ("Table made")
    return render_template ("signup.html")

@app.route("/signupcomplete", methods = ['POST'])
def signupcomplete():

    username = request.form['username']
    password = request.form['password']

    if username == "" or password == "":
        headline = "Please complete both fields"
        return render_template ("index.html", headline=headline)
    
    else:

        db.execute ("INSERT INTO users (username, password) VALUES (:username, :password)",
         {"username": username, "password": password})
        db.commit()

        headline = "Signup Successful"
        return render_template ("index.html", headline=headline)

@app.route("/loginsuccess", methods = ['POST'])
def loginsuccess():
    
    usernamelog = request.form['usernamelog']
    passwordlog = request.form['passwordlog']

    #logcommand = ('SELECT * FROM users WHERE (username = 'usernamelog' AND password = 'passwordlog')')

    if db.execute('SELECT * FROM users WHERE (username = :usernamelog AND password = :passwordlog)', {"usernamelog": usernamelog, "passwordlog": passwordlog}).rowcount == 1:

    #if login == 1
        return render_template ("search.html")
    
    else:
        return render_template ("index.html", headline="Username or password incorrect")


@app.route("/logout")
def logout():
    
    return "Project 1: TODO"


@app.route("/search")
def search():
    
    return "Project 1: TODO"


@app.route("/hello", methods=["GET", "POST"])
def hello():
    if request.method == "GET":
        return "Please submit form properly"
    else:
        name = request.form.get("name")
        return render_template("index.html", headline=name)

    
