from fastapi import FastAPI
from pydantic import BaseModel
from support_agent import SupportAIAgent
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
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
