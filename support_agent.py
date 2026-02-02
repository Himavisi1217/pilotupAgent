from typing import List, Dict
from datetime import datetime
import uuid

class SupportAIAgent:
    def __init__(self, name: str):
        self.id = str(uuid.uuid4())
        self.name = name
        self.role = "Customer Support AI Officer"
        self.system_prompt = f"""
You are {self.name}, a professional AI customer support officer.
Your goals:
- Resolve customer issues accurately
- Be polite, calm, and helpful
- Escalate only when necessary
- Never hallucinate information
"""
        self.memory: List[Dict] = []

    def store_memory(self, user_msg: str, ai_msg: str):
        self.memory.append({
            "user": user_msg,
            "ai": ai_msg,
            "timestamp": datetime.utcnow().isoformat()
        })

    def think(self, user_message: str) -> str:
        """
        This is where the LLM would be called.
        Replace mock logic with OpenAI / Claude / local model.
        """
        if "refund" in user_message.lower():
            return "I understand your concern. Let me check your order details and refund policy."
        
        return "Thanks for reaching out. Could you please provide more details so I can assist you better?"

    def respond(self, user_message: str) -> str:
        ai_response = self.think(user_message)
        self.store_memory(user_message, ai_response)
        return ai_response
