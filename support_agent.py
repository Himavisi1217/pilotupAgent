import os
from datetime import datetime
from typing import List, Dict
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class SupportAIAgent:
    def __init__(self, name: str):
        self.name = name
        self.role = "Customer Support AI Officer"
        self.memory: List[Dict] = []

        self.system_prompt = f"""
You are {self.name}, a professional AI customer support officer.
Rules:
- Be polite and concise
- Never invent facts
- Ask for clarification if needed
- Escalate complex issues
"""

    def respond(self, user_message: str) -> str:
        messages = [{"role": "system", "content": self.system_prompt}]

        # short-term memory
        for m in self.memory[-5:]:
            messages.append({"role": "user", "content": m["user"]})
            messages.append({"role": "assistant", "content": m["ai"]})

        messages.append({"role": "user", "content": user_message})

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.4
        )

        ai_reply = response.choices[0].message.content

        self.memory.append({
            "user": user_message,
            "ai": ai_reply,
            "time": datetime.utcnow().isoformat()
        })

        return ai_reply
