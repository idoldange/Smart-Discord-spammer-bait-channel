import os
import json
import aiohttp
import console
from config import model_name, url

OPENAI_API_KEY = json.loads(os.getenv("OPENAI_API_KEY", "[]")) if os.getenv("OPENAI_API_KEY") else []

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
    
    # Try each URL and model combination with failover
    for idx, api_url in enumerate(url):
        current_model = model_name[idx] if idx < len(model_name) else model_name[0]
        payload = {
            "model": current_model,
            "messages": messages,
            "temperature": 0.2
        }
        
        # Try each API key for this URL/model pair
        for KEY in OPENAI_API_KEY:
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {KEY}"
            }
            async with aiohttp.ClientSession() as session:
                try:
                    async with session.post(api_url, headers=headers, json=payload) as response:
                        if response.status >= 400:
                            error_text = await response.text()
                            console.log(f"Error from {current_model}: HTTP {response.status}: {error_text}", "ERROR", send=True)
                            continue
                        data = await response.json()
                        if data and data.get('choices'):
                            return data['choices'][0]['message']['content'].strip()
                        else:
                            console.log(f"OpenAI response format unexpected.\n```{data}```", "ERROR", send=True)
                            continue
                except aiohttp.ClientError as e:
                    console.log(f"Error connecting to OpenAI ({current_model}): {e}", "ERROR", send=True)
                    continue
                except Exception as e:
                    console.log(f"Unknown error ({current_model}): {e}", "ERROR", send=True)
                    continue
    
    console.log("All API attempts failed", "ERROR", send=True)
    return ""