import os
from datetime import datetime
from typing import List, Dict
from dotenv import load_dotenv

# Importing OpenAI SDK; fallback to legacy `openai` module where available
try:
    from openai import OpenAI
except Exception:
    OpenAI = None

load_dotenv()

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
- Ask clarifying questions if needed
- Escalate complex issues
"""

    def respond(self, user_message: str) -> str:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            return "❌ OpenAI API key not configured. Please set OPENAI_API_KEY in your .env file."

        # Development shortcut: set OPENAI_API_KEY=dev to avoid external calls
        if api_key == "dev":
            ai_reply = (
                "Hi — I'm running in dev mode. I can simulate helpful, supportive replies. "
                "Tell me more about the issue and I'll help you step-by-step."
            )
            self.memory.append({
                "user": user_message,
                "ai": ai_reply,
                "time": datetime.utcnow().isoformat()
            })
            return ai_reply

        messages = [{"role": "system", "content": self.system_prompt}]

        # short-term memory (last 5)
        for m in self.memory[-5:]:
            messages.append({"role": "user", "content": m["user"]})
            messages.append({"role": "assistant", "content": m["ai"]})

        messages.append({"role": "user", "content": user_message})

        ai_reply = ""

        try:
            # Prefer the new OpenAI client if available
            if OpenAI is not None:
                client = OpenAI(api_key=api_key)
                # new-style chat completions
                if hasattr(client, "chat") and hasattr(client.chat, "completions"):
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=messages,
                        temperature=0.4,
                        max_tokens=512,
                    )
                    # Try multiple response shapes for compatibility
                    try:
                        ai_reply = response.choices[0].message.content
                    except Exception:
                        try:
                            ai_reply = response["choices"][0]["message"]["content"]
                        except Exception:
                            ai_reply = str(response)
                else:
                    # Last-resort: try `responses` or simple string conversion
                    try:
                        resp = client.responses.create(model="gpt-4o-mini", input=messages, temperature=0.4)
                        ai_reply = getattr(resp, "output", str(resp))
                    except Exception:
                        ai_reply = "Sorry, couldn't parse AI response format."
            else:
                # Fallback to legacy openai package interface if installed
                import openai as _openai
                _openai.api_key = api_key
                resp = _openai.ChatCompletion.create(model="gpt-4o-mini", messages=messages, temperature=0.4, max_tokens=512)
                try:
                    ai_reply = resp.choices[0].message.content
                except Exception:
                    ai_reply = getattr(resp.choices[0], 'text', str(resp))

        except Exception as e:
            print("❌ OpenAI error:", e)
            ai_reply = "Sorry, the AI service is temporarily unavailable."

        # store in short-term memory
        self.memory.append({
            "user": user_message,
            "ai": ai_reply,
            "time": datetime.utcnow().isoformat()
        })

        return ai_reply
