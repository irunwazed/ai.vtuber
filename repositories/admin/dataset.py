from libs.database import conn


def get(page, per_page):
  cursor = conn.cursor()
  cursor.execute(f'SELECT * FROM datasets limit {per_page} offset {((page-1)*per_page)}')
  columns = [column[0] for column in cursor.description]  # Ambil nama kolom
  rows = cursor.fetchall()
  return [dict(zip(columns, list(row))) for row in rows]


def save(question, answer, source, document_id, created_by):
  cursor = conn.cursor()
  cursor.execute('''
  INSERT INTO datasets (question, answer, source, status, document_id, created_by)
  VALUES (?, ?, ?, 1, ?, ?)
  ''', (question, answer, source, document_id, created_by))
  conn.commit()

def update(id, question, answer, source):
  cursor = conn.cursor()
  cursor.execute('''
  UPDATE datasets
  SET question = ?, answer = ?, source = ?
  WHERE id = ?
  ''', (question, answer, source, id))  # Pass id as the third parameter
  conn.commit()



def delete(id):
  cursor = conn.cursor()
  cursor.execute('''
  DELETE FROM datasets WHERE id = ?
  ''', (id,))
  conn.commit()

def get_by_name(question):
  cursor = conn.cursor()
  cursor.execute('''
  SELECT * FROM datasets WHERE question = ?
  ''', (question,))
  rows = cursor.fetchall()
  result = None
  if rows:
    for row in rows:
      result = {
          'id': row[0],
          'question': row[1],
          'answer': row[2],
      }

  return result

def get_jumlah():
    cursor = conn.cursor()
    cursor.execute('''
    SELECT COUNT(*) FROM datasets
    ''')
    count = cursor.fetchone()[0] 
    return count

def get_jumlah_by_document(document_id):
    cursor = conn.cursor()
    cursor.execute('''
    SELECT COUNT(*) FROM datasets where document_id = ?
    ''', (document_id,))
    count = cursor.fetchone()[0] 
    return count