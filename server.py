from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
import uvicorn
from fastapi.staticfiles import StaticFiles



app = FastAPI()
# Mount the static directory for serving files like CSS, JS, etc.
app.mount("/assets", StaticFiles(directory="assets"), name="assets")

# Initialize Jinja2Templates with the 'templates' directory
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9002)
