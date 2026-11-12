import os
import openai
from dotenv import load_dotenv
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

if OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY

def generate_casual_reply(user_message: str, bot_name: str = "hermes-demo"):
    """Call OpenAI ChatCompletion to generate a short casual Vietnamese reply.
    Returns the assistant text or None on error.
    """
    if not OPENAI_API_KEY:
        # fallback canned replies if no API key
        canned = [
            "Ơ, kể nghe đi: hôm nay sao thế?",
            "Hihi, tui có câu chuyện ngắn: có con gà...",
            "Tui rảnh lắm, nói đi, tui lắng nghe mà."
        ]
        import random
        return random.choice(canned)

    try:
        prompt_system = f"You are a casual, slightly sarcastic Vietnamese AI called {bot_name}. Keep replies short (1-2 sentences). Avoid asking for personal data or giving medical/legal advice."
        messages = [
            {"role": "system", "content": prompt_system},
            {"role": "user", "content": user_message}
        ]
        resp = openai.ChatCompletion.create(model=MODEL, messages=messages, max_tokens=120, temperature=0.8)
        return resp.choices[0].message.content.strip()
    except Exception as e:
        print("OpenAI error:", e)
        return None
