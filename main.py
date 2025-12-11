import discord
from dotenv import load_dotenv
import os
import console
from config import *
if lm_api not in ["gemini", "groq", "lm_studio", "openai"]:
  console.log("Unsupported LM/LLM selected in config.py! Supported LMs/LLMs are: gemini, groq, lm_studios, openai", "ERROR")
  exit(1)
load_dotenv()
GEMINI_API_KEY=os.getenv("GEMINI_API_KEY")
DISCORD_TOKEN=os.getenv("DISCORD_TOKEN")
lm_studio_port=os.getenv("lm_studio_port")
lm_studio_ip=os.getenv("lm_studio_ip")
print("still in dev")
