import aiohttp
import console
import os
lm_studio_ip = os.getenv("lm_studio_ip")
lm_studio_port = os.getenv("lm_studio_port")
url = f"http://{lm_studio_ip}:{lm_studio_port}/api/v0/chat/completions"
async def send_request(sys_instruction: str, prompt: str, attach: dict, model: str, max_retries: int) -> str:
  headers = {
    "Content-Type": "application/json"
  }
  attachment = ""
  for att in attach:
    attachment += {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{att}"}}
  payload = {
    "model": model,
    "messages": [
      {"role": "system", "content": sys_instruction},
      {"role": "user", "content":[
          {"type": "text", "text": prompt},
          (attachment if attachment else {})
    ],
      }
    ],
    "temperature": 0.2,
    "max_tokens": 512,
    "top_p": 0.9,
    "frequency_penalty": 0,
    "presence_penalty": 0,
    "stop": ["\n"]
  }
  try:
   async with aiohttp.ClientSession() as session:
     async with session.post(url, json=payload, headers=headers) as response:
      if response.status == 200:
       data = await response.json()
       return data['choices'][0]['message']['content'].strip()
      else:
       console.log(f"LM Studio API returned status code {response.status}", "ERROR", send=True)
       return "Error: Unable to process the request."
  except Exception as e:
   console.log(f"Error in LM Studio request: {e}", "ERROR", send=True)
   return "Error: Unable to process the request."