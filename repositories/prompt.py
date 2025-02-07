from libs import llm,clear

def create_dataset_by_context(document):
    prompt = """
    Berdasarkan dokumen berikut, buatkan 10 pertanyaan yang membutuhkan penjelasan mendalam dan kompleks. 
    Pertanyaan tersebut harus mencakup berbagai aspek dari informasi yang ada dalam dokumen. Pertanyaan bisa bersifat analitis, interpretatif, atau menjelaskan hubungan antar bagian dari dokumen. Harap pastikan bahwa pertanyaan tersebut tidak hanya berfokus pada fakta, tetapi juga mengajak untuk berpikir lebih jauh dan menyeluruh.

    Dokumen:
    """ + document + """

    
    Berikan jawaban dengan format Array dibawah ini:
    [
        {"question": "pertanyaan pertama"},
        {"question": "pertanyaan kedua"},
        {"question": "pertanyaan ketiga"},
        ...
    ]
    
    """
    data = llm.ollama_chat(prompt)
    return clear.extract_data_from_text(data)


