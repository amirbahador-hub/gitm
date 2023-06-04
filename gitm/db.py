import sqlite3

conn = sqlite3.connect('pattern.db')

def migrate():
    conn.execute('''CREATE TABLE COMPANY(
                    ID INT PRIMARY KEY    NOT NULL,
                    REGEX                 CHAR(50),
                    DESCRIPTION           TEXT    NOT NULL,
                    EMOJI                 CHAR(50)
                    );''')