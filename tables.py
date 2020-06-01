import csv
import os

from sqlalchemy import create_engine, Table, Column, Integer, String
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():
    
    engine.execute ('CREATE TABLE "users" ('
        'username VARCHAR NOT NULL,'
        'password VARCHAR NOT NULL,'
        'userID VARCHAR NOT NULL,'
        'PRIMARY KEY (userID));') 

    print ("Table made")

if __name__ == "__main__":
    main()


def TableMake():
    query = """
        CREATE TABLE "users" (
        username VARCHAR NOT NULL,
        'password VARCHAR NOT NULL,
        userID VARCHAR NOT NULL,
        PRIMARY KEY (userID));
        """

    db.execute (query) 
    db.commit()

    
