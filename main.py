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

from models import Course

def add_courses(session, course_list):
    """Add courses to the database."""
    print("Adding courses...")
    for course in course_list:
        id = uuid.uuid4()

        session.add(Course(
            id=id,
            course=course[0],
            title=course[1],
            subjectArea=course[2],
            discord=course[3]
        ))

def print_database(session):
    """Print the contents of the database."""
    print("Courses:")
    for course in session.query(Course):
        print(course.id, course.course, course.title, course.subjectArea, course.discord)

def delete_course(session):
    """Delete all courses."""
    print("Deleting courses...")
    session.query(Course).delete()

def delete_table(session):
    """Delete the courses table."""
    print("Deleting table...")
    Course.__table__.drop(session.bind)

def create_table(session):
    """Create the courses table."""
    print("Creating table...")
    Course.__table__.create(session.bind)

import json

if __name__ == '__main__':
    load_dotenv()
    db_uri = os.getenv('DATABASE_URL').replace("postgresql://", "cockroachdb://")
    try:
        engine = create_engine(db_uri, connect_args={"application_name":"docs_simplecrud_sqlalchemy"})
    except Exception as e:
        print("Failed to connect to database.")
        print(f"{e}")

    with open('./courses.json', 'r') as file:
        data = json.load(file)

    courses_list = []
    for course in data['data']['SIS_Course']:
        courses_list.append((course['displayName'], course['title'], course['subjectArea']['description'], ''))

    # Create the table.
    #run_transaction(sessionmaker(bind=engine), create_table)
    
    # Delete the table.
    #run_transaction(sessionmaker(bind=engine), delete_table)

    # Add courses to the database.
    #run_transaction(sessionmaker(bind=engine), lambda s: add_courses(s, courses_list))

    # Prints the contents of the database.
    #run_transaction(sessionmaker(bind=engine), print_database)

    # Delete all courses.
    #run_transaction(sessionmaker(bind=engine), delete_classes)
