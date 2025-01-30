# from tinydb import TinyDB, Query # type: ignore

# db = TinyDB("./datasets/datasets_jdih.json")
# query = Query()

# tableAturan = db.table("aturan")

# db.insert({'name': 'Alice', 'age': 25})
# db.insert({'name': 'Bob', 'age': 30})

# User = Query()
# print(db.search(User.age > 25))


import sqlite3

# Membuat koneksi ke database (akan dibuat jika belum ada)
conn = sqlite3.connect('ai.db')


def create_table():
  cursor = conn.cursor()
  cursor.execute('''
  CREATE TABLE IF NOT EXISTS documents (
      id INTEGER PRIMARY KEY,
      name TEXT NOT NULL,
      context TEXT,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  )
  ''')
  conn.commit()

def insert_document(name, context):
  cursor = conn.cursor()
  cursor.execute('''
  INSERT INTO documents (name, context)
  VALUES (?, ?)
  ''', (name, context))
  conn.commit()

def fetch_all_documents():
  cursor = conn.cursor()
  cursor.execute('SELECT * FROM documents')
  rows = cursor.fetchall()
  result = []
  for row in rows:
    result.append(row)
  return result

def get_by_name(name):
  cursor = conn.cursor()
  cursor.execute('''
  SELECT * FROM documents WHERE name = ?
  ''', (name,))
  rows = cursor.fetchall()
  result = None
  if rows:
    for row in rows:
      result = {
          'id': row[0],
          'name': row[1],
          'context': row[2],
      }
  else:
    print(f"No records found for name: {name}")

  return result
  


create_table()