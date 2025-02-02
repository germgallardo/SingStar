import psycopg2
import os

# Setting initial Database variables
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")

# Checks if credentials exists or throws an error
if not all([DB_NAME, DB_USER, DB_PASSWORD]):
    raise ValueError("Missing Credentials for database name, user or password.")