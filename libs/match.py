

from sklearn.feature_extraction.text import TfidfVectorizer # type: ignore
from sklearn.metrics.pairwise import cosine_similarity # type: ignore
from libs import stop_words


from transformers import BertTokenizer, BertModel # type: ignore
import torch # type: ignore
import numpy as np # type: ignore

model_name = "bert-base-uncased"
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertModel.from_pretrained(model_name)



def match_with_cosine_similarity(documents, query, top_k=3):

  vectorizer = TfidfVectorizer(stop_words=stop_words.stop_words_indonesian)
  tfidf_matrix = vectorizer.fit_transform(documents + [query])
  
  cosine_similarities = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])
  isJudul = False
  for i in cosine_similarities:
    for j in i:
      if float(j) > 0.4:
        isJudul = True

  if not isJudul:
    return []
  

  similar_indices = cosine_similarities[0].argsort()[-top_k:][::-1]

  relevant_docs = [documents[i] for i in similar_indices]
  
  return relevant_docs



def sentence_to_bert_vector(sentence):
    inputs = tokenizer(sentence, return_tensors="pt", truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).squeeze().numpy()

def match_with_bert(documents, query, top_k=3):
    short_vector = sentence_to_bert_vector(query)
    matches = []
    
    for long_text in documents:
        long_vector = sentence_to_bert_vector(long_text)
        similarity = np.dot(short_vector, long_vector) / (np.linalg.norm(short_vector) * np.linalg.norm(long_vector))
        if similarity > 0.2:  # Ambang batas kesamaan
            matches.append((long_text, similarity))
    
    # similar_indices = matches.argsort()[0][-top_k:][::-1]
    
    return matches