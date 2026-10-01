import sqlite3
def initialize_database(database_path):
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS employees(
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    role TEXT NOT NULL )                  
    """)
    connection.close()