import psycopg2
import os
import sys

# Setting initial Database environment variables
DB_NAME = os.getenv("DB_NAME", "postgres")  # default postgresql database
DB_USER = os.getenv("DB_USER", "")  # for testing add default postgresql username & password
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")

# Checks if all credentials exist or throws an error
if not all([DB_NAME, DB_USER, DB_PASSWORD]):
    raise ValueError(f"Missing Credentials for database name, user or password {[DB_NAME, DB_USER, DB_PASSWORD]}.")

def database_connection(database="postgres"):
    try:
        # Makes a connection with the postgresql database
        connection = psycopg2.connect(
            database = database,
            user = DB_USER,
            password = DB_PASSWORD,
            host = DB_HOST,
            port = DB_PORT
            )
        print("Connection was successfully done!")

        connection.autocommit = True # commits the changes to the database, needs to be here

        # Defines a cursor object to run our queries
        cursor = connection.cursor()
        # Apply `execute` and define our query
        cursor.execute("SELECT version()")
        # With `fetchone` we retrieve the result in a single row tuple (fetchall returns all rows and fetchmany only those that we want)
        db_version = cursor.fetchone()[0]
        print(f"PostgreSQL Database version: {db_version}")
        return connection
    
    except psycopg2.OperationalError as e:
        sys.exit(f"There was an error when trying to reach the database: {e}")


def create_database():
    try:
        connection = database_connection()

        cursor = connection.cursor()

        # Creates the database `youtube_music_tracker` in case it does not exist
        if cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'youtube_music_tracker'"):
            print(f"[+] Database 'youtube_music_tracker' already exists.\n")
        else:
            print(f"[-] Database 'youtube_music_tracker' not found, attempting to create...")
            cursor.execute(f"CREATE DATABASE youtube_music_tracker;")
            print(f"[+] Database 'youtube_music_tracker' was successfully created!")

        cursor.close()
        connection.close()

    except Exception as e:
        sys.exit(f"There was an error when trying to create the database: {e}")



def create_table():
    try:
        connection = database_connection(database="youtube_music_tracker")
        print(connection)

        cursor = connection.cursor()    # creates a cursor object to execute SQL queries

        # Creates the table for playlists inside the `youtube_music_tracker`database
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS playlists (
                playlist_id VARCHAR(150) PRIMARY KEY,
                playlist_name VARCHAR(100) NOT NULL,
                number_videos SMALLINT NOT NULL,
                creation_date DATE NOT NULL,
                last_update DATE NOT NULL,
                description VARCHAR(1000) NULL
            )
        """)
        
        cursor.close()
        connection.close()
        print("Playlist Table successfully created!")

    except Exception as e:
        print(f"Error while creating the database: {e}")


def remove_table():
    pass


def display_table():
    pass


if __name__ == "__main__":
    print("Hello!")
    #database_connection()
    create_database()
    create_table()