import sqlite3

conn = sqlite3.connect('sorular.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS sorular (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    metin TEXT NOT NULL
)
''')

# Örnek veri ekleme
sorular = []

cursor.executemany("INSERT INTO sorular (metin) VALUES (?)", sorular)
conn.commit()
conn.close()
