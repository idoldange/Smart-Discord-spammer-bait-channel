import time
starttime_a = time.time()
import discord
from dotenv import load_dotenv
import os
import console
import datetime
from discord.ext import commands
from config import *

if lm_api not in ["gemini", "groq", "lm_studio", "openai"]:
  console.log("Unsupported LM/LLM selected in config.py! Supported LMs/LLMs are: gemini, groq, lm_studios, openai", "ERROR")
  exit(1)
  
load_dotenv()
DISCORD_TOKEN=os.getenv("DISCORD_TOKEN")

client = commands.Bot(command_prefix="/", intents=discord.Intents.all())

@client.event

async def on_ready():
    console.log(f'Bot logged in as {client.user}', "INFO")
    console.log((f'Using LM/LLM: {lm_api}' if lm_api else "Double-check disabled"), "INFO")
    starttime = time.time() - starttime_a
    console.log(f'Done, start time:{starttime}', "INFO", send=True)
    
async def on_message(message):
    if message.author == client.user:
        return
    channel = message.channel
    if channel.id in bait_channel:
        console.log(f"Received message in bait channel {channel.id} from {message.author}: {message.content}", "INFO", is_user_msg=True, send=True, client=client)
        if not use_lm:
          console.log("LM/LLM double-check is disabled, automatically ban.", "INFO", send=True, client=client)
          reason = "spam"
          try:
            guild = message.guild
            member = message.author
            bantime = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            await member.send(f"[{bantime}]You have been banned from {guild.name} for the following reason: {reason}\nYou can appeal against this ban at https://hangdongwibu.io/appeal")
            await guild.ban(member, reason=reason)
          except Exception as e:
            console.log(f"Failed to ban user: {e}", "ERROR", send=True, client=client)
        

if __name__ == "__main__":
    client.run(DISCORD_TOKEN)