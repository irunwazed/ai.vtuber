from transformers import BertTokenizer, BertModel
import torch
import numpy as np  

# Memuat model BERT pra-latih dan tokenizer
model_name = "bert-base-uncased"
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertModel.from_pretrained(model_name)

# Fungsi untuk mendapatkan vektor kalimat dengan BERT
def sentence_to_bert_vector(sentence):
    inputs = tokenizer(sentence, return_tensors="pt", truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).squeeze().numpy()

def match_with_bert(short_text, long_texts):
    short_vector = sentence_to_bert_vector(short_text)
    matches = []
    
    for long_text in long_texts:
        long_vector = sentence_to_bert_vector(long_text)
        similarity = np.dot(short_vector, long_vector) / (np.linalg.norm(short_vector) * np.linalg.norm(long_vector))
        if similarity > 0.2:  # Ambang batas kesamaan
            matches.append((long_text, similarity))
    
    return matches

# Contoh Penggunaan
short_text = "saya suka python programming"
long_texts = [
    "Saya belajar Python dan JavaScript.",
    "Python adalah bahasa pemrograman yang hebat.",
    "Saya suka bermain sepak bola.",
    "Saya benci python programming",
    "siapa saya ini?"
]
matches = match_with_bert(short_text, long_texts)
for match, score in matches:
    print(f"Matched Text: {match} with Similarity Score: {score}")
