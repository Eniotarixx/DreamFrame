from fastapi import FastAPI # use to create the API
from pydantic import BaseModel # use to check data input
from dream_frame import generate_image  # my script to adapte 
import uuid # use to create a unique filename
import os # use to create a directory
from fastapi.responses import HTMLResponse


app = FastAPI() # create an instance of the FastAPI class

class PromptRequest(BaseModel): # endpoint Generate want to receive a prompt
    prompt: str

# POST to /generate endpoint then execute the function generate
@app.post("/generate") 
def generate(prompt_request: PromptRequest): # receive the prompt

    prompt = prompt_request.prompt # get the prompt from the request
    filename = f"output_{uuid.uuid4().hex[:8]}.png" # create a unique filename
    path = f"/app/outputs/{filename}" # create a path to the file
    
    os.makedirs("/app/outputs", exist_ok=True) # create a directory if it doesn't exist
    generate_image(prompt, path) #call the function generate_image from the dream_frame.py file
    return {"message": "Image generated", "file": filename} # return the filename

@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <html>
        <head>
            <title>DreamFrame Prompt</title>
        </head>
        <body>
            <h1>Enter your prompt</h1>
            <form action='/generate' method='post'>
                <input type='text' name='prompt' placeholder='Type your prompt here' required style='width:300px;'>
                <button type='submit'>Generate</button>
            </form>
        </body>
    </html>
    """