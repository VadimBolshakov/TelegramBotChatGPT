# This is the database module
import sqlite3
import datetime


def start_db() -> None:
    """Create users and requests tables."""
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


def add_user(user_id: int, first_name: str, full_name: str, user_name: str,
             date_registration: datetime) -> None:
    """Add the new user to the users table."""
    with sqlite3.connect('database.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as db:
        cursor = db.cursor()
        user = (user_id, first_name, full_name, user_name, date_registration)
        query = """INSERT INTO users (user_id, first_name, full_name, user_name, date_registration) VALUES (?, ?, ?, 
        ?, ?) """
        cursor.execute(query, user)
        db.commit()


def get_user(user_id: int) -> tuple:
    """Get the user from the users' table by id."""
    with sqlite3.connect('database.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as db:
        cursor = db.cursor()
        query = " SELECT * FROM users WHERE user_id=? "
        cursor.execute(query, (user_id,))
        return cursor.fetchone()


def get_all_users() -> list:
    """Get all users from the users' table."""
    with sqlite3.connect('database.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as db:
        cursor = db.cursor()
        query = " SELECT * FROM users "
        cursor.execute(query)
        return cursor.fetchall()


def get_requests_count() -> int:
    """Get the total number of requests from the requests' table."""
    with sqlite3.connect('database.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as db:
        cursor = db.cursor()
        query = " SELECT COUNT(*) FROM requests "
        cursor.execute(query)
        return cursor.fetchone()[0]


def add_request(user_id: int, date: datetime, num_tokens: int, status: int) -> None:
    """Add the new request to the requests' table."""
    with sqlite3.connect('database.db', detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES) as db:
        cursor = db.cursor()
        request = (user_id, date, num_tokens, status)
        query = """INSERT INTO requests (user_id, date, num_tokens, status) VALUES (?, ?, ?, ?) """
        cursor.execute(query, request)
        db.commit()


if __name__ == '__main__':
    pass
