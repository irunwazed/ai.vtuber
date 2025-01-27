from libs import pdf, helpers, clustering, pdf, database
from repositories import chatbot, datasets
import json


# datasets.create_datasets_rag("./datasets/jdih", "./datasets/datasets_jdih.json")
# datasets.set_label("./datasets/datasets_jdih.json")


datasets.add_datasets_rag("./datasets/jdih", "./datasets/datasets_jdih.json")


# db = database.db

# db.insert({"name": "testing2"})