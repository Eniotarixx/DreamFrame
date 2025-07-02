from fastapi import FastAPI, Request, Form, File, UploadFile # use to create the API
from pydantic import BaseModel # use to check data input
from dream_frame import generate_image  # my script to adapte 
import uuid # use to create a unique filename
import os # use to create a directory
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles


app = FastAPI() # create an instance of the FastAPI class
templates = Jinja2Templates(directory="templates")
app.mount("/outputs", StaticFiles(directory="/app/outputs"), name="outputs")

class PromptRequest(BaseModel): # endpoint Generate want to receive a prompt
    prompt: str

# POST to /generate endpoint then execute the function generate
@app.post("/generate") 
def generate(prompt: str = Form(...), image: UploadFile = File(...)):
    filename = f"output_{uuid.uuid4().hex[:8]}.png"
    output_dir = "/app/outputs"
    os.makedirs(output_dir, exist_ok=True)
    path = f"{output_dir}/{filename}"

    image_path = f"{output_dir}/uploaded_{uuid.uuid4().hex[:8]}.png"
    with open(image_path, "wb") as buffer:
        buffer.write(image.file.read()) # can now use image_path as needed

    generate_image(prompt, path, image_path)  #  want to adapt this to use image_path if needed
    #return RedirectResponse(url=f"/?file={filename}", status_code=303)
    return RedirectResponse(url="/?file=output_inpaint.png", status_code=303)
# GET to / endpoint then return the index.html file
@app.get("/", response_class=HTMLResponse)
def read_root(request: Request, file: str = None):
    return templates.TemplateResponse("index.html", {"request": request, "file": file})