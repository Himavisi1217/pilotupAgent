import os
from datetime import datetime
from typing import List, Dict
import openai
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    # Don't raise here to keep the app from crashing on import in dev; handle at call time instead
    OPENAI_API_KEY = None
else:
    openai.api_key = OPENAI_API_KEY


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

        if not OPENAI_API_KEY:
            # Friendly error when key not set
            ai_reply = "OpenAI API key not configured. Please set OPENAI_API_KEY in your .env file."
            self.memory.append({"user": user_message, "ai": ai_reply, "time": datetime.utcnow().isoformat()})
            return ai_reply

        try:
            # Use the standard OpenAI ChatCompletion interface
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",
                messages=messages,
                temperature=0.4,
                max_tokens=512,
            )

            # safety: validate structure
            ai_reply = response["choices"][0]["message"]["content"]

        except Exception as e:
            # Print the exception so it's visible in uvicorn logs, and return a safe message
            print("OpenAI API call failed:", repr(e))
            ai_reply = "Sorry, I'm having trouble accessing the AI service right now. Please try again later."

        self.memory.append({
            "user": user_message,
            "ai": ai_reply,
            "time": datetime.utcnow().isoformat()
        })

        return ai_reply
