import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect("app.db")
cursor = conn.cursor()

# Check for existing tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables:", tables)

# Check the contents of the alembic_version table (if it exists)
cursor.execute("SELECT * FROM alembic_version;")
version = cursor.fetchone()
print("Alembic version:", version)

# Close the connection
conn.close()
