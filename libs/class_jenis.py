import pandas as pd # type: ignore
import joblib # type: ignore
from sklearn.feature_extraction.text import CountVectorizer # type: ignore
from sklearn.model_selection import train_test_split # type: ignore
from sklearn.neural_network import MLPClassifier # type: ignore
from sklearn.metrics import classification_report # type: ignore
import json
from libs import helpers


PATH_MODEL = "models/mlp_jenis"

def training(path_json, epochs = 5000):


  datasets = helpers.load_json(path_json)

  data = pd.DataFrame(datasets)

  X = data['text']
  y = data['label']

  vectorizer = CountVectorizer()
  X_vectorized = vectorizer.fit_transform(X)

  X_train, X_test, y_train, y_test = train_test_split(X_vectorized, y, test_size=0.2, random_state=42)

  model = MLPClassifier(hidden_layer_sizes=(100,), max_iter=epochs, random_state=42) 
  model.fit(X_train, y_train)

  joblib.dump(model, PATH_MODEL+'_model.pkl')
  joblib.dump(vectorizer, PATH_MODEL+'_vectorizer.pkl')

  y_pred = model.predict(X_test)
  print(classification_report(y_test, y_pred))

def check_class_once(text):
  # text = "text"
  loaded_model = joblib.load(PATH_MODEL+'_model.pkl')
  loaded_vectorizer = joblib.load(PATH_MODEL+'_vectorizer.pkl')

  example_vectorized = loaded_vectorizer.transform([text])
  example_predictions = loaded_model.predict(example_vectorized)
  return example_predictions[0]


def check_class(texts):
  # texts = ["text", "text"]

  loaded_model = joblib.load(PATH_MODEL+'_model.pkl')
  loaded_vectorizer = joblib.load(PATH_MODEL+'_vectorizer.pkl')

  example_vectorized = loaded_vectorizer.transform(texts)
  example_predictions = loaded_model.predict(example_vectorized)
  result = []
  for text, label in zip(texts, example_predictions):
    result.append({
      "text":text ,
      "label": str(label)
    })
  return result