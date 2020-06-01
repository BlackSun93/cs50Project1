from flask_sqlalchemy import flask_sqlalchemy

db = SQLAlchemy()

class users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)


class review(db.Model):
    __tablename__ = "reviews"
    revid = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    review = db.Column(db.String)
    stars = db.Column(db.Integer(5), nullable=False)
    #Project asks for raw sql to be used with .execute and .commit sqlalchemy methods so I wont be using this