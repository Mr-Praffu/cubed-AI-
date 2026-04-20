from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

# Load API key
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

app = FastAPI()

# Enable CORS (frontend connection)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request schema
class ChatRequest(BaseModel):
    message: str


# Optional root route (to avoid 404 confusion)
@app.get("/")
def home():
    return {"message": "Backend is running"}


# Chat route
@app.post("/chat")
async def chat(req: ChatRequest):
    try:
        url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={API_KEY}"

        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": req.message}
                    ]
                }
            ]
        }

        response = requests.post(url, json=payload)
        data = response.json()

        print("FULL RESPONSE:", data)

        if "candidates" in data:
            reply = data["candidates"][0]["content"]["parts"][0]["text"]
            return {"reply": reply}
        else:
            return {"error": data}

    except Exception as e:
        print("ERROR:", e)
        return {"error": str(e)}