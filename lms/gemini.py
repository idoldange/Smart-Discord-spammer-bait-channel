import aiohttp
import console
import os
import json
import base64
import mimetypes
import asyncio
FULL_GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_KEY = json.loads(FULL_GEMINI_API_KEY) if FULL_GEMINI_API_KEY else ""

async def ask_gemini(model_name: str = "gemini-2.5-flash-lite", text: str = "", attachments: list = None, temperature: float = 0.5, max_retries: int = 3, sys_prompt: str = "") -> dict:
  text = text.strip()

  retry_delay = 2.0
  keys = GEMINI_API_KEY
  base_url = "https://generativelanguage.googleapis.com/v1beta"


  def build_payload():
    parts = []
    if text:
      parts.append({"text": text})

    if attachments:
      for att in attachments:
        if isinstance(att, dict) and "inline_data" in att:
          parts.append(att)
        else:
          file_path, mime_type = att if isinstance(att, tuple) else (
            att,
            mimetypes.guess_type(att)[0] or "application/octet-stream"
          )
          try:
            with open(file_path, "rb") as f:
              base64_data = base64.b64encode(f.read()).decode("utf-8")
            parts.append({
              "inline_data": {
                "mime_type": mime_type,
                "data": base64_data
              }
            })
          except Exception as e:
            continue
          
    full_parts = []

    def _append_part(candidate):
      if isinstance(candidate, dict):
        if "text" in candidate or "inline_data" in candidate:
          full_parts.append(candidate)
          return
        try:
          full_parts.append({"text": json.dumps(candidate, ensure_ascii=False)})
        except Exception:
          full_parts.append({"text": str(candidate)})
        return
      if isinstance(candidate, str):
        full_parts.append({"text": candidate})
        return
      try:
        full_parts.append({"text": str(candidate)})
      except Exception:
        pass

    for p in parts:
      _append_part(p)
    return {
      "safetySettings": [ {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"}, {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"}, {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"}, {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"} ],
      "system_instruction": {"parts": [{"text": sys_prompt}]},
      "contents": [{"parts": full_parts}],
      "generationConfig": {"temperature": temperature}
    }


  async def send_request(model: str, api_key: str, payload: dict):
    full_model_name = f"models/{model}" if not model.startswith("models/") else model
    url = f"{base_url}/{full_model_name}:generateContent"
    headers = {"Content-Type": "application/json"}
    params = {"key": api_key}

    session = aiohttp.ClientSession()
    for attempt in range(3):  
      try:
        resp = await session.post(
          url, headers=headers, params=params, json=payload, timeout=600
        )
        return resp
      except (aiohttp.ClientConnectionError, aiohttp.ClientConnectorError, aiohttp.ServerDisconnectedError) as e:
        console.log(f"Connection error on attempt {attempt+1}/3: {e}", "WARN", send=True)
        if attempt < 2:
          await asyncio.sleep(1 * (attempt + 1))
        else:
          console.log(f"Request failed after 3 attempts: {e}", "ERROR", send=True)
          return None
      except Exception as e:
        console.log(f"Request exception với key={api_key}: {e}", "ERROR", send=True)
        return None


  def is_max_token_error(error_data: dict) -> bool:
    """Phát hiện prompt vượt max token dựa vào message/code."""
    if not error_data:
      return False
    text = json.dumps(error_data).lower()
    keywords = [
      "context_length_exceeded",
      "maximum context length",
      "max token",
      "too many tokens",
      "prompt too long",
      "exceeds the context",
      "context",
      "250000",
      "token"
    ]
    return any(kw in text for kw in keywords)


  async def try_model(model: str):
    payload = build_payload()

    for attempt in range(1, max_retries + 1):
      for key_index, API_KEY in enumerate(keys):
        console.log(f"[{model}] Thử key {key_index+1}/{len(keys)}...", "INFO")

        resp = await send_request(model, API_KEY, payload)
        if not resp:
          continue

        if resp.status == 200:
          data = await resp.json()
          return data

        try:
          data = await resp.json()
        except:
          data = {}

        if resp.status == 429:
          if is_max_token_error(data):
            console.log(f"[{model}] Vượt max token, fallback", "WARN", send=True)
            return {"error": "MAX_TOKEN", "status": 429}
          console.log(f"[{model}] Rate limit, thử key khác", "WARN", send=True)
          continue

        if resp.status == 503:
          console.log(f"[{model}] 503 Service Unavailable, retry", "WARN", send=True)
          continue 

        if resp.status in (400, 500):
          console.log(f"[{model}] 400/500, retry (attempt {attempt})", "WARN", send=True)
          continue

        text = await resp.text()
        console.log(f"[{model}] HTTP {resp.status}: {text}", "WARN", send=True)
        return {"error": text, "status": resp.status}

      console.log(f"[{model}] Hết key, sleep {retry_delay}s (attempt {attempt})", "WARN", send=True)
      await asyncio.sleep(retry_delay)

      try:
         text = await resp.text()
      except:
        text = "<no body>"

      url = str(resp.url)
      safe_url = url.split("?key=")[0] + "?key=***" if "?key=" in url else url

      return {
        "error": f"HTTP {resp.status} - {safe_url} - {text[:500]}",
        "status": resp.status
      }


  result = await try_model(model_name)

  return result