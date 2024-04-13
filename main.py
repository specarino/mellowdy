import asyncio
from twitch import Bot
from authenticator import authenticate

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(authenticate())

    bot = Bot()
    bot.run()