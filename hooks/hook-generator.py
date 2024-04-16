import os
from dotenv import load_dotenv

load_dotenv()

env = {
    "SPOTIPY_CLIENT_ID": os.getenv("SPOTIPY_CLIENT_ID"),
    "SPOTIPY_CLIENT_SECRET": os.getenv("SPOTIPY_CLIENT_SECRET"),
    "SPOTIPY_REDIRECT_URI": os.getenv("SPOTIPY_REDIRECT_URI"),
    "TWITCH_APP_ID": os.getenv("TWITCH_APP_ID"),
    "TWITCH_APP_SECRET": os.getenv("TWITCH_APP_SECRET")
}


content = """import os

env = {
"""

for key, value in env.items():
    content += f"    '{key}': '{value}',\n"

content += """}

# Set environment variables
for key, value in env.items():
    os.environ[key] = value
"""


with open('hook-env-loader.py', 'w') as file:
    file.write(content)

print("hook-env-loader.py has been created successfully!")
