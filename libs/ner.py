import spacy # type: ignore
from spacy.training.example import Example # type: ignore
from libs import helpers

PATH_MODEL = "models/ner_bkn"

def training(text, epoch = 10):
  # contoh
  # text = "Joko Widodo adalah Presiden Indonesia."
  # entities = [{"entities": [(0, 12, "PERSON"), (27, 36, "GPE")]}]

  entities_datasets = helpers.load_json("datasets/datasets_ner_entity.json")
  entities_train = []
  for entity_label in entities_datasets:
    label = entity_label["label"]
    for entity in entity_label["val"]:
      entities_train.append({"entities": generate_dataset(text, entity, label)})

  nlp = spacy.blank("id")

  if "ner" not in nlp.pipe_names:
      ner = nlp.add_pipe("ner")
  else:
      ner = nlp.get_pipe("ner")

  for annotations in entities_train:
    for ent in annotations.get("entities"):
      ner.add_label(ent[2])

  optimizer = nlp.begin_training()
  # epoch = 10 
  for i in range(epoch):
    print(f"Epoch {i+1}/{epoch}")
    losses = {}
    for annotations in entities_train:
      example = Example.from_dict(nlp.make_doc(text), annotations)
      nlp.update([example], drop=0.35, losses=losses)
    print(f"Losses: {losses}")

  nlp.to_disk(PATH_MODEL)

def search_entities(text):
  nlp = spacy.load(PATH_MODEL)
  doc = nlp(text)
  entities = []
  for ent in doc.ents:
    entities.append({
      "text": ent.text,
      "label": ent.label_
    })
  return entities

def generate_dataset(text, entity, label):
  # contoh
  # text = "Pegawai BKN"
  # entity = "BKN"
  # label = "ORG"
  entities_train_tmp = []
  all = helpers.find_all(text, entity)
  for ent in all:
    entities_train_tmp.append((ent, (ent+len(entity)), label))
  return entities_train_tmp

def training_lib():
  # Load multilingual model
  nlp = spacy.load("xx_ent_wiki_sm")

  # Teks contoh
  text = """
  Joko Widodo lahir pada tanggal 21 Juni 1961 di Surakarta, Jawa Tengah. 
  Beliau adalah Presiden Republik Indonesia ke-7.
  """
  # text = """
  # Pak Zudan sekarang adalah kepala BKN
  # """

  # Proses teks
  doc = nlp(text)

  # Ekstraksi entitas
  print("Entitas dalam teks:")
  for ent in doc.ents:
    print(f"{ent.text} ({ent.label_})")

def search_entities_json(text):
  entities_datasets = helpers.load_json("datasets/datasets_ner_entity.json")
  result = []
  for entities in entities_datasets:
    for entity in entities["val"]:
      if text.lower().find(entity.lower()) != -1:
        result.append({
          "text": entity,
          "label": entities["label"],
          "desc": entities["desc"]
        })
  return result
