import sqlite3

conn = sqlite3.connect("stylesense.db")
cursor = conn.cursor()

# USERS TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT,
    skin_tone TEXT
)
""")

# CLOTHES TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS clothes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    type TEXT,
    color TEXT,
    brand TEXT
)
""")

# WEEKLY PLAN TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS weekly_plan (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    day TEXT,
    top_desc TEXT,
    bottom_desc TEXT
)
""")

# SAMPLE USER (for login testing)
cursor.execute("""
INSERT OR IGNORE INTO users VALUES
('admin','1234','Medium')
""")

conn.commit()
conn.close()

print("Database created successfully ✅")