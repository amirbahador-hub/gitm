import sqlite3


def exec_sql(sql:str):
    try:
        sqliteConnection = sqlite3.connect('database.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        cursor.execute(sql)
        sqliteConnection.commit()
        print("Record deleted successfully")

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to run the sql", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("sqlite connection is closed")