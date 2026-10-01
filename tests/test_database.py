from database import initialize_database
import sqlite3
def test_initialize_database_employee_table(tmp_path):
    database_path = tmp_path/ "test_shiftflow.db"
    initialize_database(database_path)
    
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='employees';")
    result = cursor.fetchone()
    assert result == ('employees',)
    connection.close()

