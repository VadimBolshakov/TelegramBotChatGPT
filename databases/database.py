# This is the database module
import sqlite3
import datetime


# Create users and requests tables
def start_db() -> None:
    with sqlite3.connect('database.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as db:
        cursor = db.cursor()
        query = """ CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            user_id INTEGER,
            first_name TEXT,
            full_name TEXT,
            user_name TEXT,
            date_registration TIMESTAMP
        )"""
        cursor.execute(query)
        db.commit()

        query = """ CREATE TABLE IF NOT EXISTS requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            user_id INTEGER,
            date TIMESTAMP,
            num_tokens INTEGER, 
            status INTEGER
        )"""
        cursor.execute(query)
        db.commit()


# Add the new user to the users table
def add_db_user(user_id: int, first_name: str, full_name: str, user_name: str,
                date_registration: datetime) -> None:
    """

    :rtype: object
    """
    with sqlite3.connect('database.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as db:
        cursor = db.cursor()
        user = (user_id, first_name, full_name, user_name, date_registration)
        query = """INSERT INTO users (user_id, first_name, full_name, user_name, date_registration) VALUES (?, ?, ?, 
        ?, ?) """
        cursor.execute(query, user)
        db.commit()


# Get the user from the users' table by his id
def get_db_user(user_id: int) -> tuple:
    with sqlite3.connect('database.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as db:
        cursor = db.cursor()
        query = " SELECT * FROM users WHERE user_id=? "
        cursor.execute(query, (user_id,))
        return cursor.fetchone()


# Add the new request to the requests table
def add_db_request(user_id: int, date: datetime, num_tokens: int, status: int) -> None:
    with sqlite3.connect('database.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as db:
        cursor = db.cursor()
        request = (user_id, date, num_tokens, status)
        query = """INSERT INTO requests (user_id, date, num_tokens, status) VALUES (?, ?, ?, ?) """
        cursor.execute(query, request)
        db.commit()


if __name__ == '__main__':
    pass
