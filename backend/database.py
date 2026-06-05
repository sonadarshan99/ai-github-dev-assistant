import sqlite3

conn = sqlite3.connect(
    "memory.db",
    check_same_thread=False
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS analyses(

id INTEGER PRIMARY KEY,

commit_message TEXT,

risk_score INTEGER,

category TEXT
)
""")

conn.commit()