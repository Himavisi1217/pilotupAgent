from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from support_agent import SupportAIAgent

app = FastAPI()

# ✅ CORS (keep this)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Serve frontend folder
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

# ✅ Serve UI at root
@app.get("/")
def serve_ui():
    return FileResponse("frontend/index.html")

agent = SupportAIAgent("Pilot Support Agent")

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
def chat(req: ChatRequest):
    reply = agent.respond(req.message)
    return {
        "agent": agent.name,
        "reply": reply
    }
