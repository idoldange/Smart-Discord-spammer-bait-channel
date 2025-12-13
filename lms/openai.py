import os
import aiohttp
import console
from model_config import OPENAI_MODEL_NAME
import json
OPENAI_API_KEY = json.load(os.getenv("OPENAI_API_KEY")) if os.getenv("OPENAI_API_KEY") else ""
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"

async def call_openai(prompt: str, system_prompt: str = "", attachments: list = None) -> str:
    messages = []
    if system_prompt:
        messages.append({
            "role": "system",
            "content": system_prompt
        })
    user_content = []
    if attachments:
        for att in attachments:
            user_content.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/png;base64,{att}"
                }
            })
    user_content.append({
        "type": "text",
        "text": prompt
    })
    messages.append({
        "role": "user",
        "content": user_content
    })
    
    payload = {
        "model": OPENAI_MODEL_NAME,
        "messages": messages,
        "temperature": 0.2
    }
    
    for KEY in OPENAI_API_KEY:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {KEY}"
        }
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(OPENAI_API_URL, headers=headers, json=payload) as response:
                    if response.status >= 400:
                        error_text = await response.text()
                        return f"Lỗi HTTP {response.status}: {error_text}"
                    data = await response.json()
                    if data and data.get('choices'):
                        return data['choices'][0]['message']['content'].strip()
                    else:
                        console.log(f"OpenAI response format unexpected.\n```{data}```", "ERROR", send=True)
                        continue
            except aiohttp.ClientError as e:
                console.log(f"Error connecting to OpenAI: {e}", "ERROR", send=True)
                continue
            except Exception as e:
                console.log(f"Unknown error: {e}", "ERROR", send=True)
                continue