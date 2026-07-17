import mysql.connector

from services.config import DB_CONFIG


def get_connection():
    """
    Return a MySQL connection.

    Raises:
        mysql.connector.Error
            If connection fails.
    """

    return mysql.connector.connect(
        host=DB_CONFIG["host"],
        port=DB_CONFIG["port"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        database=DB_CONFIG["database"],
    )