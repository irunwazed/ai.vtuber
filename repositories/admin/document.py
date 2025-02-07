from libs.database import conn

def get(page, per_page):
  cursor = conn.cursor()
  cursor.execute(f'SELECT * FROM documents order by created_at desc limit {per_page} offset {((page-1)*per_page)}')
  columns = [column[0] for column in cursor.description]  # Ambil nama kolom
  rows = cursor.fetchall()
  return [dict(zip(columns, list(row))) for row in rows]

def save(name, name_value, context, context_value, url, type):
  cursor = conn.cursor()
  cursor.execute('''
  INSERT INTO documents (name, name_value, context, context_value, url, type)
  VALUES (?, ?, ?, ?, ?, ?)
  ''', (name, name_value, context, context_value, url, type))
  conn.commit()

def update(id, name, name_value, context, context_value, url, type):
  cursor = conn.cursor()
  cursor.execute('''
  UPDATE documents
  SET name = ?, name_value = ?, context = ?, context_value = ?, url = ?, type = ?
  WHERE id = ?
  ''', (name, name_value, context, context_value, url, type, id))  # Pass id as the third parameter
  conn.commit()


def delete(id):
  cursor = conn.cursor()
  cursor.execute('''
  DELETE FROM documents WHERE id = ?
  ''', (id,))
  conn.commit()

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
          'url': row[3]
      }

def get_by_id(id):
  cursor = conn.cursor()
  cursor.execute('''
  SELECT * FROM documents WHERE id = ?
  ''', (id,))
  rows = cursor.fetchall()
  result = None
  if rows:
    for row in rows:
      result = {
          'id': row[0],
          'name': row[1],
          'context': row[2],
          'url': row[3]
      }

  return result

def get_jumlah():
    cursor = conn.cursor()
    cursor.execute('''
    SELECT COUNT(*) FROM documents
    ''')
    count = cursor.fetchone()[0] 
    return count