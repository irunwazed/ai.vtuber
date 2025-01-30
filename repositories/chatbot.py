from libs import class_jenis, ner, llm, helpers
from repositories.datasets import search_documents

def chat_bkn(question):
  jenis = class_jenis.check_class_once(question)
  entities = ner.search_entities_json(question)

  print("jenis", jenis)

  result = "Maaf saya tidak mengerti"
  try:
    if jenis == "greeting":
      result = llm.ollama_chat(f"Buat kalimat salam secara singkat dengan jabatan salam ini: {question}")
    elif len(entities) > 0:
      # if jenis == "request_what":
      #   result = llm.ollama_chat("Jelaskan secara singkat mengenai ini : "+entities[0]["desc"])
      if jenis == "request_who":
        result = llm.ollama_chat("Jelaskan secara singkat Siapa itu : "+entities[0]["text"]+" dengan deskripsi singkat "+ entities[0]["desc"])
     
    # else:
    if result == "Maaf saya tidak mengerti":
      result = chat_rag(question) # llm.ollama_chat("Jawab secara singkat pertanyaan ini : "+question)
  except Exception as e:
    print("ERROR : ", e)
  return result

def test_chat(question):
  text = """
  <div class="wpb_wrapper">
        <p>Prof. Dr. Zudan Arif Fakrulloh, SH., M.H lahir pada tahun 1969 di Sleman, Daerah Istimewa Yogyakarta. Zudan mendapatkan gelar S1 Hukum di Universitas Sebelas Maret pada tahun 1992, kemudian melanjutkan studi S2 pada jurusan Ilmu Hukum di Universitas Diponegoro serta lulus pada tahun 1995. Setelah itu melanjutkan studi S3 Doktor Ilmu Hukum di universitas yang sama dan mendapatkan gelar Doktor Ilmu Hukum pada tahun 2001.</p>
  <p>Zudan mengawali kariernya di pemerintahan pada tahun 1999 yaitu menjadi CPNS di Badan Diklat Kementerian Dalam Negeri. Selang beberapa tahun setelah menjadi PNS, Ia mendapat kepercayaan untuk menjabat sebagai Kasubid Kader PD Bid. Kader Profesionalisme Kediklatan Pusdiklat Kader &amp; Pengemb. Kepemimp. Bandiklat, kemudian naik dan mendapat kepercayaan sebagai Kabag. Penyusunan Rancangan Peraturan Perundang-undangan pada Biro Hukum Sekretaris Jenderal Kementerian Dalam Negeri.</p>
  <p>Seiring berjalannya waktu, Zudan mengemban beberapa jabatan penting di lingkungan Kementerian Dalam Negeri baik untuk jabatan JPT Pratama maupun JPT Madya, seperti Kepala Biro Hukum Pada Sekretariat Jenderal, Staf Ahli Bidang Hukum, Politik dan Hubungan Antar Lembaga Pada Sekretariat Jenderal Kementerian Dalam Negeri, Direktur Jenderal Kependudukan dan Pencatatan Sipil pada Kementerian Dalam Negeri dan terakhir pada jabatan Sekretaris Badan Nasional Pengelola Perbatasan pada Kementerian Dalam Negeri. Selain jabatan struktural di lingkungan Kementerian Dalam Negeri, Zudan juga pernah ditunjuk untuk mengisi beberapa jabatan di luar tugas utamanya sebagai PNS yaitu sebagai Penjabat Gubernur di Provinsi Gorantalo, Provinsi Sulawesi Barat dan terakhir di Provinsi Sulawesi Selatan.</p>
  <p>Selain aktif di pemerintahan, Zudan juga aktif sebagai dosen di beberapa universitas baik negeri maupun swasta, di antaranya dengan menjadi dosen S2 Ilmu Hukum STIH Iblam Jakarta, dosen S2 Ilmu Hukum Universitas Tanjung Pura Pontianak, dosen Magister Manajemen STIE STIEKUBANK Semarang, dosen S2 dan S3 Ilmu Hukum Untag Surabaya, dosen S2 Ilmu Hukum Universitas Borobudur Jakarta, dosen S3 Ilmu Hukum Undip dan beberapa universitas lainnya.</p>
  <p>Pada bulan Januari 2025, Presiden Prabowo Subianto menunjuk Zudan sebagai Kepala BKN berdasarkan Keputusan Presiden Nomor 188/TPA Tahun 2024 tentang Pengangkatan Pejabat Pimpinan Tinggi Utama di Lingkungan Badan Kepegawaian Negara (BKN). Ia resmi menjabat Kepala Badan Kepegawaian Negara sejak 07 Januari 2025.</p>
      </div>
  """
  context = helpers.clean_html(text)

  prompt = f"""
    Gunakan informasi berikut untuk menjawab pertanyaan secara langsung dan jelas:
    {context}

    Pertanyaan:
    {question}

    Jawaban:"""
  
  result = "Maaf saya tidak mengerti"
  try:
    result = llm.ollama_chat(prompt)
  except Exception as e:
    print("ERROR : ", e)
  return result

def chat_with_context(context, question):
  prompt = f"""
    Gunakan informasi berikut untuk menjawab pertanyaan secara langsung, jelas dan sangat singkat:
    {context}

    Pertanyaan:
    {question}

    Jawaban:"""
  
  result = "Maaf saya tidak mengerti"
  try:
    result = llm.ollama_chat(prompt)
  except Exception as e:
    print("ERROR : ", e)
  return result

# def chat_rag(question):
#   context = search_documents(question)
#   print("context", context[0]["name"])
#   prompt = f"""
#     Gunakan informasi berikut untuk menjawab pertanyaan secara langsung, jelas dan singkat:
#     judul dokumen:
#       {context[0]["name"]}
#     Isi:
#       {context[0]["context"]}

#     Pertanyaan:
#     {question}

#     Jawaban:"""
  
#   result = "Maaf saya tidak mengerti"
#   try:
#     result = llm.ollama_chat(prompt)
#   except Exception as e:
#     print("ERROR : ", e)
#   return result

def chat_rag(question):
    context = search_documents(question)
    print("Context retrieved from document:", context[0]["name"])
    
    prompt = f"""
    Anda adalah model bahasa yang terlatih untuk menjawab pertanyaan dengan memanfaatkan konteks dari dokumen yang relevan.
    Gunakan informasi berikut untuk memberikan jawaban yang langsung, jelas, dan singkat.

    Judul Dokumen: 
    {context[0]["name"]}

    Isi Dokumen:
    {context[0]["context"]}

    Pertanyaan:
    {question}

    Berdasarkan informasi yang diberikan dalam dokumen di atas, jawab pertanyaan ini dengan tepat. Jika jawabannya tidak ada dalam konteks, berikan respon yang jelas menjelaskan ketidaktahuan Anda.
    
    Jawaban:
    """
    
    result = "Maaf, saya tidak mengerti."
    try:
        result = llm.ollama_chat(prompt)
    except Exception as e:
        print("ERROR:", e)
    return result