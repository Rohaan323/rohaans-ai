
import gradio as gr
from groq import Groq
import os
import json

# ✅ Memory System
MEMORY_FILE = "memory.json"

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return {}

def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f)

memory = load_memory()

# ✅ Groq Client
client = Groq(api_key="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")

# ✅ Chat function
def chat_with_ai(message, chat_history):
    try:
        # Handle memory inputs
        if "my name is" in message.lower():
            name = message.split("is")[-1].strip()
            memory["name"] = name
            save_memory(memory)
            reply = f"Nice to meet you, {name}!"
            return chat_history + [[message, reply]]

        if "what is my name" in message.lower():
            name = memory.get("name", "not saved yet")
            reply = f"Your name is {name}."
            return chat_history + [[message, reply]]

        # Format for Groq
        messages = []
        for user, bot in chat_history:
            messages.append({"role": "user", "content": user})
            messages.append({"role": "assistant", "content": bot})
        messages.append({"role": "user", "content": message})

        # Get AI reply
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=messages
        )

        reply = response.choices[0].message.content
        return chat_history + [[message, reply]]

    except Exception as e:
        return chat_history + [[message, f"❌ Error: {str(e)}"]]

# ✅ Gradio UI using Blocks (works perfectly)
with gr.Blocks() as demo:
    gr.Markdown("## 🤖 Smart AI Chatbot (with Memory)")
    chatbot = gr.Chatbot()
    msg = gr.Textbox(placeholder="Type your message and press Enter...")
    clear = gr.Button("Clear")

    chat_history = gr.State([])

    def respond(message, history):
        return "", chat_with_ai(message, history)

    msg.submit(respond, [msg, chat_history], [msg, chatbot])
    clear.click(lambda: None, None, chatbot, queue=False)

demo.launch()
