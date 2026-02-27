import sqlite3

conn = sqlite3.connect('stylesense.db')
cursor = conn.cursor()

# Adjust the columns to match your 'users' table structure
try:
    cursor.execute("INSERT INTO users (username, password, skin_tone) VALUES (?, ?, ?)", 
                   ("testuser", "password123", "Fair"))
    conn.commit()
    print("User 'testuser' created successfully!")
except Exception as e:
    print(f"Error: {e} (User might already exist)")

conn.close()