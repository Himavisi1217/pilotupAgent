from fastapi import FastAPI
from pydantic import BaseModel
from support_agent import SupportAIAgent

app = FastAPI()
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
