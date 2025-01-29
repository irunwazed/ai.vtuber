from tinydb import TinyDB, Query # type: ignore

db = TinyDB("./datasets/datasets_jdih.json")
query = Query()

tableAturan = db.table("aturan")

# db.insert({'name': 'Alice', 'age': 25})
# db.insert({'name': 'Bob', 'age': 30})

# User = Query()
# print(db.search(User.age > 25))