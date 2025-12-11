import os
import glob
from datetime import datetime
import discord
from config import *
import asyncio
LOG_DIR = ".\\logs"
LOG_PER_FILE = 20
MAX_LOG_FILES = 50
if not os.path.exists(LOG_DIR):
  os.makedirs(LOG_DIR)

current_log_file = None
user_msg_count = 0

def get_new_log_file():
  timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
  return os.path.join(LOG_DIR, f"log-{timestamp}.log")

class AnsiColor:
  RESET = "\033[0m"
  GREEN = "\033[32m"
  BLUE = "\033[34m"
  RED = "\033[31m"
  YELLOW = "\033[33m"
  CYAN = "\033[36m"
  MAGENTA = "\033[35m"
  GRAY = "\033[90m"

COLOR_MAP = {
  "INFO": AnsiColor.GREEN,
  "DEBUG": AnsiColor.CYAN,
  "ERROR": AnsiColor.RED,
  "WARN": AnsiColor.YELLOW,
  "BOT": AnsiColor.GRAY
}

async def send_log_to_discord(client: discord.Client, channel_id: list, message: str, level="INFO"):
  color_map = {
    "INFO": 0x00FF00,
    "DEBUG": 0x00FFFF,
    "ERROR": 0xFF0000,
    "WARN": 0xFFFF00,
    "BOT": 0x808080
  }
  color = color_map.get(level.upper(), 0xFFFFFF)
  embed = discord.Embed(description=message, color=color)
  timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
  embed.set_footer(text=f"Logged at {timestamp}")
  for channelid in channel_id:
    channel = client.get_channel(channelid)
    if channel:
      await channel.send(embed=embed)

def log(message: str, level="INFO", is_user_msg=False, send=False, client: discord.Client = None):
  global current_log_file, user_msg_count, debug_enabled, log_channel
  if level.upper() == "DEBUG" and not debug_enabled:
    return
  if send_logs_to_discord and log_channel and send and client is not None:
    asyncio.create_task(send_log_to_discord(client=client, channel_id=log_channel, message=message, level=level))

  timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
  line = f"[{timestamp}] [{level}]: {message}"

  color = COLOR_MAP.get(level.upper(), "")
  if level.upper() != "DEBUG" or debug_enabled:
    print(f"{color}{line}{AnsiColor.RESET}")

  if is_user_msg:
    user_msg_count += 1

  if current_log_file is None or user_msg_count > LOG_PER_FILE:
    current_log_file = get_new_log_file()
    user_msg_count = 0
    with open(current_log_file, "a", encoding="utf-8") as f:
      f.write("-------\n")

    files = sorted(glob.glob(os.path.join(LOG_DIR, "log-*.log")))
    if len(files) > MAX_LOG_FILES:
      for old_file in files[:-MAX_LOG_FILES]:
        os.remove(old_file)

  with open(current_log_file, "a", encoding="utf-8") as f:
    f.write(f"{color}{line}\n")
   
