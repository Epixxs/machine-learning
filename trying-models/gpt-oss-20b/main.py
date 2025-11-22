import os
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from openai import OpenAI

# Set up environment variables 
os.environ["HF_TOKEN"] = "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"

app = FastAPI()

#OpenAI client
client = OpenAI(
    base_url="https://router.huggingface.co/v1",
    api_key=os.environ["HF_TOKEN"],
)

class ChatRequest(BaseModel):
    message: str

@app.post("/api/chat")
async def chat(request: ChatRequest):
    try:
        completion = client.chat.completions.create(
            model="openai/gpt-oss-20b:groq",
            messages=[
                {
                    "role": "user",
                    "content": request.message
                }
            ],
        )
        return {"response": completion.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_index():
    return FileResponse("static/index.html")
