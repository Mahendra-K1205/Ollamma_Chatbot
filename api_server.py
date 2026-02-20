"""
FastAPI Backend - Can be deployed to cloud services
Proxies requests to Ollama server
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import os

app = FastAPI(title="Ollama Chatbot API")

# CORS for Vercel frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OLLAMA_URL = os.getenv("OLLAMA_API_URL", "http://localhost:11434")


class ChatRequest(BaseModel):
    message: str
    model: str = "llama3.2:latest"
    history: list = []


class ChatResponse(BaseModel):
    message: str
    success: bool


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/models")
def get_models():
    try:
        response = requests.get(f"{OLLAMA_URL}/api/tags", timeout=10)
        response.raise_for_status()
        models = response.json().get("models", [])
        return {"models": [m["name"] for m in models], "success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        messages = request.history + [{"role": "user", "content": request.message}]
        
        response = requests.post(
            f"{OLLAMA_URL}/api/chat",
            json={
                "model": request.model,
                "messages": messages,
                "stream": False
            },
            timeout=300
        )
        response.raise_for_status()
        
        result = response.json()
        return ChatResponse(
            message=result["message"]["content"],
            success=True
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
