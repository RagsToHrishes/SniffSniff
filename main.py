"""
https://www.cockroachlabs.com/docs/stable/build-a-python-app-with-cockroachdb-sqlalchemy.html
"""

import os
import uuid
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_cockroachdb import run_transaction
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from models import Class

def add_classes(session, class_list):
    """Add classes to the database."""
    print("Adding classes...")
    for class_ in class_list:
        id = uuid.uuid4()

        session.add(Class(
            id=id,
            course=class_[0],
            descrip=class_[1],
            discord=class_[2]
        ))

def print_database(session):
    """Print the contents of the database."""
    print("Classes:")
    for class_ in session.query(Class):
        print(class_.id, class_.course, class_.descrip, class_.discord)

def delete_classes(session):
    """Delete all classes."""
    print("Deleting classes...")
    session.query(Class).delete()

if __name__ == '__main__':
    load_dotenv()
    db_uri = os.getenv('DATABASE_URL').replace("postgresql://", "cockroachdb://")
    try:
        engine = create_engine(db_uri, connect_args={"application_name":"docs_simplecrud_sqlalchemy"})
    except Exception as e:
        print("Failed to connect to database.")
        print(f"{e}")

    # Add classes to the database.
    #run_transaction(sessionmaker(bind=engine), lambda s: add_classes(s, [('CS 170', 'Efficient Algorithms and Intractable Problems', ''), ('CS 188', 'Introduction to Artificial Intelligence', '')]))

    # Prints the contents of the database.
    #run_transaction(sessionmaker(bind=engine), print_database)

    # Delete all classes.
    #run_transaction(sessionmaker(bind=engine), delete_classes)
