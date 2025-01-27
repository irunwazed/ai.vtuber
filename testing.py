from libs import pdf, helpers, clustering, pdf
from repositories import chatbot, datasets
import json


datasets.create_datasets_rag("./datasets/jdih", "./datasets/datasets_jdih.json")
datasets.set_label("./datasets/datasets_jdih.json")
