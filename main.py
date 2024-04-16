import asyncio
from modules import twitch
from modules import auth

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(auth.authenticate())

    bot = twitch.Bot()
    bot.run()
