from fastapi import FastAPI, Request # type: ignore
from fastapi.responses import HTMLResponse, JSONResponse # type: ignore
from fastapi.templating import Jinja2Templates # type: ignore
from fastapi.staticfiles import StaticFiles # type: ignore
from fastapi.middleware.cors import CORSMiddleware
import uvicorn # type: ignore
from libs import helpers


from repositories import chatbot


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

# Mount the static directory for serving files like CSS, JS, etc.
app.mount("/assets", StaticFiles(directory="assets"), name="assets")

# Initialize Jinja2Templates with the 'templates' directory
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/chat", response_class=HTMLResponse)
async def chat_message(chat:str):
    message = chatbot.chat_bkn(chat)
    # message = chatbot.chat_rag(chat)
    result =  {"message": message}
    return JSONResponse(content=result)

@app.get("/chat-data", response_class=HTMLResponse)
async def chat_message(chat:str):
    # data = helpers.load_file("data.txt")
    message = chatbot.chat_rag(chat)
    result =  {"message": message}
    return JSONResponse(content=result)

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=9003, reload=True)
