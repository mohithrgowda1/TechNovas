import sqlite3

def init_db():
    conn = sqlite3.connect('stylesense.db')
    cursor = conn.cursor()

    # SHEET 1 & 3: Users
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        skin_tone TEXT
    )''')

    # SHEET 4: Wardrobe
    cursor.execute('''CREATE TABLE IF NOT EXISTS clothes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        type TEXT,
        color TEXT,
        brand TEXT,
        FOREIGN KEY(username) REFERENCES users(username)
    )''')

    # SHEET 5: Weekly Sets
    cursor.execute('''CREATE TABLE IF NOT EXISTS weekly_plan (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        day TEXT,
        top_desc TEXT,
        bottom_desc TEXT
    )''')

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()