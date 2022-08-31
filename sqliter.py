import config
import sqlite3

path_db = 'database.db'


def connect():
    conn = sqlite3.connect(config.path_db)
    cursor = conn.cursor()
    return conn, cursor


def create_tables():
    conn, cursor = connect()
    try:
        cursor.execute(f'CREATE TABLE admins (user_id INTEGER)')
        cursor.execute(f'CREATE TABLE words (word TEXT)')
        conn.commit()
    except:
        pass


def exists_admin(user_id):
    with sqlite3.connect(config.path_db) as c:
        b = c.execute("SELECT * FROM admins").fetchall()[0]
        result = False
        for i in b:
            if i == int(user_id):
                result = True
        return result


def get_admins():
    with sqlite3.connect(config.path_db) as c:
        return c.execute("SELECT * FROM admins").fetchall()


def new_word(word):
    with sqlite3.connect(config.path_db) as c:
        c.execute("INSERT INTO words ('word') VALUES(?)", (word,)).fetchone()


def del_word(word):
    with sqlite3.connect(config.path_db) as c:
        c.execute("DELETE FROM words WHERE word=?", (word,))


def add_admin(user_id):
    with sqlite3.connect(config.path_db) as c:
        c.execute("INSERT INTO admins ('user_id') VALUES(?)", (user_id,)).fetchone()


def del_admin(user_id):
    with sqlite3.connect(config.path_db) as c:
        c.execute("DELETE FROM admins WHERE user_id=?", (user_id,))


def get_words():
    with sqlite3.connect(config.path_db) as c:
        return c.execute("SELECT * FROM words").fetchall()
