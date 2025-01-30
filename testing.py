from libs import pdf, helpers, clustering, pdf, database
from repositories import chatbot, datasets
import json

# datasets.create_datasets_rag("./datasets/jdih", "./datasets/datasets_jdih.json")
# datasets.set_label("./datasets/datasets_jdih.json")
datasets.add_datasets_rag("./datasets/jdih")


# data = database.fetch_all_documents()
# for i in data:
#   print(i[1])

# for i in range(200):
#   datasets.add_datasets_rag("./datasets/jdih")



