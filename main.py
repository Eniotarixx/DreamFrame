from fastapi import FastAPI
from pydantic import BaseModel
from dream_frame import generate_image  # à créer ou adapter
import uuid
import os

app = FastAPI()

class PromptRequest(BaseModel):
    prompt: str

@app.post("/generate")
def generate(prompt_request: PromptRequest):
    prompt = prompt_request.prompt
    filename = f"output_{uuid.uuid4().hex[:8]}.png"
    path = f"/app/outputs/{filename}"
    
    os.makedirs("/app/outputs", exist_ok=True)
    generate_image(prompt, path)  # implémente cette fonction
    return {"message": "Image generated", "file": filename}