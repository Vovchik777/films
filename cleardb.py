import sqlite3

conn = sqlite3.connect('films.db')
cursor = conn.cursor()
#cursor.execute("DELETE from films WHERE year = 0")z
cursor.execute("VACUUM")
conn.commit()