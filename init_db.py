import sqlite3

conn = sqlite3.connect('patients.db')
c = conn.cursor()

c.execute('DROP TABLE IF EXISTS patients')

c.execute("""
    CREATE TABLE patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        symptoms TEXT,
        advice TEXT,
        drugs TEXT,
        notes TEXT
    )
""")

conn.commit()
conn.close()
print("✅ Updated patients table created.")
