from fastapi import FastAPI, Request, File, UploadFile # type: ignore
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse # type: ignore
from fastapi.templating import Jinja2Templates # type: ignore
from fastapi.staticfiles import StaticFiles # type: ignore
from fastapi.middleware.cors import CORSMiddleware # type: ignore
from fastapi.exceptions import HTTPException # type: ignore
import uvicorn # type: ignore
from libs import helpers, llm, pdf, const, clear, match
from repositories.admin import document, dataset
from repositories import prompt,  datasets
from pydantic import BaseModel # type: ignore
import os
from typing import List, Dict
import shutil


from repositories import chatbot

class RequestSaveDocument(BaseModel):
    name: str
    context: str
    url: str
    type:int

class RequestUpdateDocument(BaseModel):
    name: str
    context: str
    url: str
    type:int
    id: int|None


class RequestSaveDataset(BaseModel):
    question: str
    answer: str
    source: str

class RequestUpdateDataset(BaseModel):
    question: str
    answer: str
    source: str
    id: int|None

class RequestSaveDocumentDatasets(BaseModel):
    data:List[Dict[str, str]]
    document_id:str



class RequestPrompt(BaseModel):
    prompt: str
    clear:bool

class RequestText(BaseModel):
    text: str


app = FastAPI()

origins = [
    "http://localhost:3000",  # Contoh untuk aplikasi frontend lokal
    "http://example.com",     # Domain lain yang diizinkan
    "*",                      # Gunakan "*" untuk mengizinkan semua origin (tidak direkomendasikan untuk produksi)
]

# Menambahkan middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Daftar asal yang diizinkan
    allow_credentials=True, # Jika Anda mengizinkan pengiriman cookies atau token melalui CORS
    allow_methods=["*"],    # Metode HTTP yang diizinkan (GET, POST, dll.)
    allow_headers=["*"],    # Header yang diizinkan
)

app.mount("/assets", StaticFiles(directory="assets"), name="assets")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/testing", response_class=HTMLResponse)
async def read_root(request: Request):
    # name = "PERBERSAMA KEPALA LAN NO.16 TAHUN 2014 DAN KEPALA BKN NO.16 TAHUN 2014 - KETENTUAN PELAKSANAAN PERMENPAN DAN RB NO.45 TAHUN 2013 TENTANG JF ANALIS KEBIJAKAN DAN AK"
    
    # data = document.get_by_name(name)

    # respon = prompt.create_dataset_by_context(data["context"])


    # query = "jelaskan tentang undang undang"
    # datasets.match_documents(query)

    directory_path = './datasets/KELOMPOK PPU'

    files_and_dirs = os.listdir(directory_path)

    data = []
    for label in files_and_dirs:
        if label != ".DS_Store":
            files = os.listdir(directory_path+'/'+label)
            for file in files:
                data.append({
                    "label": label,
                    "file": file
                })


    # for doc in data:
    #     label = doc["label"]
    #     file = doc["file"]
    #     if ".pdf" in file:
    #         name = file.replace(".pdf", "")
    #         filename = clear.generate_random_string(12)+ "_" + clear.space_to_under(file)

    #         path_file = directory_path+"/"+label+"/"+file
    #         to_file = const.UPLOAD_DIR_DOCUMENT / filename

    #         shutil.copy(path_file, to_file)

    #         context = "" # pdf.pdf_ocr_to_text(path_file)

    #         name_value = helpers.numpy_to_json_string(match.sentence_to_bert_vector(name))
    #         context_value = helpers.numpy_to_json_string(match.sentence_to_bert_vector(context))


    label = data[0]["label"]
    file = data[0]["file"]
    if ".pdf" in file:
        name = file.replace(".pdf", "")
        filename = clear.generate_random_string(12)+ "_" + clear.space_to_under(file)

        path_file = directory_path+"/"+label+"/"+file
        to_file = const.UPLOAD_DIR_DOCUMENT / filename

        shutil.copy(path_file, to_file)

        context = pdf.pdf_ocr_to_text(path_file)

        name_value = helpers.numpy_to_json_string(match.sentence_to_bert_vector(name))
        context_value = helpers.numpy_to_json_string(match.sentence_to_bert_vector(context))


    document.save(name, name_value, context, context_value, filename, 1)

    result = {
        "data": {
            "label": label,
            "file": file,
            "filename": filename,
            "name": name,
            "context": context,
            "name_value": name_value,
            "context_value": context_value,
        }
    }
    return JSONResponse(content=result)




@app.get("/chat", response_class=HTMLResponse)
async def chat_message(chat:str):
    # message = chatbot.chat_bkn(chat)
    message = chatbot.chat_rag(chat)
    result =  {"message": message}
    return JSONResponse(content=result)

@app.get("/chat-ollama", response_class=HTMLResponse)
async def chat_ollama(chat:str):
    message = llm.ollama_chat(chat)
    result =  {"message": message}
    return JSONResponse(content=result)

@app.get("/chat-data", response_class=HTMLResponse)
async def chat_message(chat:str):
    # data = helpers.load_file("data.txt")
    message = chatbot.chat_rag(chat)
    result =  {"message": message}
    return JSONResponse(content=result)

@app.post("/doc-to-text", response_class=HTMLResponse)
async def chat_message(file:UploadFile):
    filename = clear.generate_random_string(12)+ "_" + clear.space_to_under(file.filename)
    path_file = await helpers.upload(file, filename)
    text = pdf.pdf_ocr_to_text(path_file)
    result =  {
        "name": file.filename,
        "desc": text,
        "filename": filename
    }
    return JSONResponse(content=result)

@app.post("/text-to-array", response_class=HTMLResponse)
async def chat_message(req:RequestText):
    text = clear.remove_think_tags(req.text)
    text = clear.extract_data_from_text(text)
    result =  {
        "array": text
    }
    return JSONResponse(content=result)


@app.get("/prompt/doc", response_class=HTMLResponse)
async def admin(request: Request):
    result =  {
        "template": [
            ""
        ]
    }
    return JSONResponse(content=result)

@app.get("/admin", response_class=HTMLResponse)
async def admin(request: Request):
    return templates.TemplateResponse("admin.html", { "request": request})

@app.get("/admin/monitoring", response_class=HTMLResponse)
async def admin(request: Request):
    result =  {
        "documents": document.get_jumlah(),
        "datasets": dataset.get_jumlah()
    }
    return JSONResponse(content=result)


@app.post("/admin/prompt", response_class=HTMLResponse)
async def admin_documents(req: RequestPrompt):
    respon = llm.ollama_chat(req.prompt)
    if(req.clear):
       respon = clear.remove_think_tags(respon) 
    result =  {
        "respon": respon
    }
    return JSONResponse(content=result)

@app.get("/admin/documents", response_class=HTMLResponse)
async def admin_documents(request: Request, page:int=1, per_page:int=10):
    documents = document.get(page, per_page)
    for i in range(len(documents)):  # Looping through valid indices
        documents[i]["jumlah_dataset"] = dataset.get_jumlah_by_document(documents[i]["id"])
    return templates.TemplateResponse("documents.html", { "pagination": {
        "page": page,
        "per_page": per_page
    }, "request": request, "documents": documents})


@app.post("/admin/document/datasets/save", response_class=HTMLResponse)
async def document_save(body: RequestSaveDocumentDatasets):

    docu = document.get_by_id(body.document_id)

    if not docu:
        raise HTTPException(status_code=400, detail="Document tidak ada")

    for data in body.data:
        check = dataset.get_by_name(data["question"])
        if check:
            if docu["url"] == check["source"]:
                dataset.update(check["id"], data["question"], data["answer"], docu["url"])
        dataset.save(data["question"], data["answer"], docu["url"], body.document_id, "BKN Team")
    result =  {
        "message": "Berhasil simpan"
    }
    return JSONResponse(content=result)

@app.post("/admin/document/save", response_class=HTMLResponse)
async def document_save(body: RequestSaveDocument):
    check = document.get_by_name(body.name)
    if check:
        raise HTTPException(status_code=400, detail="Nama Dokumen sudah ada")
    
    name_value = helpers.numpy_to_json_string(match.sentence_to_bert_vector(body.name))
    context_value = helpers.numpy_to_json_string(match.sentence_to_bert_vector(body.context))

    document.save(body.name, name_value, body.context, context_value, body.url, body.type)
    result =  {
        "message": "Berhasil simpan"
    }
    return JSONResponse(content=result)

@app.post("/admin/document/update", response_class=HTMLResponse)
async def document_update(body: RequestUpdateDocument):
    

    name_value = helpers.numpy_to_json_string(match.sentence_to_bert_vector(body.name))
    context_value = helpers.numpy_to_json_string(match.sentence_to_bert_vector(body.context))

    document.update(body.id, body.name, name_value, body.context, context_value, body.url, body.type)
    result =  {
        "message": "Berhasil simpan"
    }
    return JSONResponse(content=result)

@app.get("/admin/document/delete/{doc_id}", response_class=HTMLResponse)
async def document_delete(doc_id:int):
    respon = document.delete(doc_id)
    result = {
        "message": "Berhasil delete"
    }
    return JSONResponse(content=result)

@app.get("/admin/datasets", response_class=HTMLResponse)
async def admin_datasets(request: Request, page:int=1, per_page:int=10):
    datasets = dataset.get(page, per_page)
    return templates.TemplateResponse("datasets.html", { "pagination": {
        "page": page,
        "per_page": per_page
    }, "request": request, "datasets": datasets})


@app.post("/admin/dataset/save", response_class=HTMLResponse)
async def document_save(body: RequestSaveDataset):
    check = dataset.get_by_name(body.question)
    if check:
        raise HTTPException(status_code=400, detail="Nama Dokumen sudah ada")
    dataset.save(body.question, body.answer, body.source, None, "BKN Team")
    result =  {
        "message": "Berhasil simpan"
    }
    return JSONResponse(content=result)

@app.post("/admin/dataset/update", response_class=HTMLResponse)
async def document_update(body: RequestUpdateDataset):
    dataset.update(body.id, body.question, body.answer, body.source)
    result =  {
        "message": "Berhasil simpan"
    }
    return JSONResponse(content=result)

@app.get("/admin/dataset/delete/{doc_id}", response_class=HTMLResponse)
async def document_delete(doc_id:int):
    respon = dataset.delete(doc_id)
    result = {
        "message": "Berhasil delete"
    }
    return JSONResponse(content=result)


@app.get("/download/{doc}", response_class=HTMLResponse)
async def document_delete(doc:str):
    path = const.UPLOAD_DIR_DOCUMENT / doc
    print("path", path)
    if os.path.exists(path):
        return FileResponse(path, filename=doc, media_type="application/pdf")
    result = {
        "error": "File Not Found"
    }
    return JSONResponse(content=result)


if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=9003, reload=True)
