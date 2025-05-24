import chainlit as cl
import google.generativeai as genai
import os
import json
from datetime import datetime
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Use correct model (v1 compatible)
model = genai.GenerativeModel("models/gemini-1.5-flash-latest")
chat = model.start_chat()
chat_history = []

@cl.on_message
async def on_message(message: cl.Message):
    response = model.generate_content(message.content)
    await cl.Message(content=response.text).send()

@cl.on_chat_start
async def on_chat_start():
    await cl.Message("👋 Hi! I'm your Gemini assistant.").send()

@cl.on_message
async def on_message(message: cl.Message):
    user_input = message.content
    timestamp = datetime.utcnow().isoformat()

    chat_history.append({
        "role": "user",
        "content": user_input,
        "timestamp": timestamp
    })

    try:
        response = chat.send_message(user_input)
        reply = response.text

        chat_history.append({
            "role": "assistant",
            "content": reply,
            "timestamp": timestamp
        })

        await cl.Message(content=reply).send()

    except Exception as e:
        await cl.Message(f"⚠️ Error: {str(e)}").send()

@cl.on_chat_end
async def on_chat_end():
    with open("chat_history.json", "w", encoding="utf-8") as f:
        json.dump(chat_history, f, indent=2, ensure_ascii=False)
