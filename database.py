import sqlite3

DB_Path = "business.db"

#Establishes a connection to the database
def get_connection():
    conn = sqlite3.connect(DB_Path)
    conn.row_factory = sqlite3.Row
    return conn

#Initializes the Database 

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    #This is where the actual SQL is placed to do operations on the DB
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            Customer_ID           INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name            TEXT NOT NULL,
            last_name             TEXT NOT NULL,
            email                 TEXT UNIQUE NOT NULL,
            number                TEXT,
            address               TEXT,
            username              TEXT UNIQUE NOT NULL,
            passwordHash          TEXT NOT NULL,
            salt                  TEXT NOT NULL,
            mustChangePassword    INTEGER NOT NULL DEFAULT 0
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            Employee_ID           INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name            TEXT NOT NULL,
            last_name             TEXT NOT NULL,
            email                 TEXT UNIQUE NOT NULL,
            username              TEXT UNIQUE NOT NULL,
            passwordHash          TEXT NOT NULL,
            salt                  TEXT NOT NULL,
            expenses              REAL NOT NULL DEFAULT 0.0
            mustChangePassword    INTEGER NOT NULL DEFAULT 0
        )
    ''')


    conn.commit()   #saves
    conn.close()    #closes connection to the database
