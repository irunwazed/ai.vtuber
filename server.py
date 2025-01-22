from fastapi import FastAPI, Request # type: ignore
from fastapi.responses import HTMLResponse, JSONResponse # type: ignore
from fastapi.templating import Jinja2Templates # type: ignore
from fastapi.staticfiles import StaticFiles # type: ignore
import uvicorn # type: ignore

from libs import helpers, llm, class_jenis
from libs import ner


def chat_bkn(question):
  jenis = class_jenis.check_class_once(question)
  entities = ner.search_entities_json(question)

  result = "Maaf saya tidak mengerti"
  try:
    if len(entities) > 0:
      if jenis == "request_what":
        result = llm.ollama_chat("Jelaskan secara singkat mengenai ini : "+entities[0]["desc"])
      elif jenis == "request_who":
        result = llm.ollama_chat("Jelaskan secara singkat Siapa itu : "+entities[0]["text"]+" dengan deskripsi singkat "+ entities[0]["desc"])
    else:
      result = llm.ollama_chat("Jawab secara singkat pertanyaan ini : "+question)
  except Exception as e:
    print("ERROR : ", e)

  return result


app = FastAPI()
# Mount the static directory for serving files like CSS, JS, etc.
app.mount("/assets", StaticFiles(directory="assets"), name="assets")

# Initialize Jinja2Templates with the 'templates' directory
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/chat", response_class=HTMLResponse)
async def chat(chat:str):
    message = chat_bkn(chat)
    result =  {"message": message}
    return JSONResponse(content=result)
    # return templates.TemplateResponse("index.html", {"request": request})

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=9002, reload=True)
