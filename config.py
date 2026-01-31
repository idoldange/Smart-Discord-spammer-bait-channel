
# =][= Configuration File =][= #

#=][= Channel for baiting spam bot =][=
bait_channel=[]

#=][= Channel for logging bot activity =][=
send_logs_to_discord=False
log_channel=[]


#=][= Enable/disable language model usage for double-check =][=
use_lm=True


#=][= Select language model API =][=
lm_api=[]
#  currently support provider: "gemini", "openrouter", "lm_studio", "openai"
#  if one fails, it will automatically try the next one in the list


#=][= Enable/disable debug messages in console/logs =][=
debug_enabled=False

#=][= API config =][=
url=["https://api.openai.com/v1/chat/completions"]
model_name=["gpt-4o"] #model MUST support multimodal image input, otherwise please turn the multimodal off.
# This supports multiple urls and model names for failover purposes
# Each url will line up with each model_name by index
# For example, url[0] will be used with model_name[0], url[1] with model_name[1], and so on.
# Make sure to have the same number of entries in both lists.
# Also make sure the API keys provided have access to the specified models. This will try all api keys for each url/model pair if fail so no need to duplicate keys for each pair.
multimodal_enabled=True  # Enable/disable multimodal (image) input support

#⠘⠻⡿⠿⠿⠿⠿⠿⠿⠿⠿⠟⠛⠛⠛⣻⡿⠋⠀⣀⣀⣀⠄⠠⣀⣠⣀⡀⠈⠻⣿⡛⠛⠛⠻⠿⠿⠿⠿⠿⠿⠿⠿⠿⠿⠋
#⠀⠀⠀⢦⣤⣴⣶⣶⠶⠶⠛⠛⢛⣩⣭⣿⠀⠀⠿⠛⠻⣿⣦⣴⣾⡞⠛⢻⠃⠀⢸⡯⣍⣙⠛⠛⠷⠶⢶⣶⣶⣤⣤⠆⠀⠀
#⠀⠀⠀⠀⠉⢡⣠⣤⣴⡶⠾⠛⣉⣵⠖⣻⣦⣤⣤⣤⣶⣌⣳⣷⣫⣶⣦⣤⣤⣤⣾⡓⢦⣍⡙⠻⠶⣶⣤⣤⣠⠈⠁⠀⠀⠀
#⠀⠀⠀⠀⠀⠀⠈⠉⣀⣤⡶⠟⠉⣠⡾⢡⡏⡽⢹⡹⣸⣟⣿⣿⡟⣷⡸⣽⢹⡝⣦⠹⣦⡈⠙⠷⣦⣄⡈⠉⠀⠀⠀⠀⠀⠀
#⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⢀⣴⡾⠋⣰⡟⣰⠇⠯⢾⡿⣼⣿⣿⣿⣹⣿⠞⠆⣷⠸⣧⠈⠻⣦⣄⠈⠉⠀⠀⠀⠀⠀⠀⠀⠀
#⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠰⠿⠁⠋⠀⠀   ⢱⢿⣿⣿⣿⡞⠀⠀⠈⠃⠹⠷⠀⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
#⠀⠀⠀⠀ ⠀⠀ ⠀⠀⠀⠀⠀⠀⠀⠀ ⠀⠀⠀ ⣀⣠⣞⡝⡟⡟⡽⡽⣦⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
#⠀⠀ ⠀⠀⠀  ⠀⠀⠀⠀ ⠀⠀⠀⠀⠀ ⠀⢰⣣⢏⠿⠹⢻⣷⠻⠽⣏⢿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
#⠀⠀⠀⠀ ⠀ ⠀ ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ ⠀⠛⠁⠀⠀⠀⠁ ⠀ ⠀⠛⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀