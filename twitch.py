from twitchio.ext import commands
import spotify
import os
from dotenv import load_dotenv

load_dotenv()

ACCESS_TOKEN = os.getenv("TW_ACCESS_TOKEN")
PREFIX=os.getenv("TW_PREFIX")
CHANNEL=os.getenv("TW_CHANNEL")

class Bot(commands.Bot):

    def __init__(self):
        super().__init__(
            token=ACCESS_TOKEN,
            prefix=PREFIX,
            initial_channels=[
                CHANNEL,
            ]
        )

    async def event_ready(self):
        print(f"Logged in as | {self.nick}")
        print(f"User ID is   | {self.user_id}")

    @commands.command(name="song", aliases=("playing", "np"))
    async def song_name(self, ctx: commands.Context):
        cmd = spotify.get_currently_playing()
        await ctx.send(cmd)
        print(f'{ctx.author.name} used "{str(ctx.message.content).strip()}" | {cmd}')

    @commands.command(name="sr", aliases=("queue", "q", "request", "play", "p"))
    async def song_request(self, ctx: commands.Context, query):
        cmd = spotify.add_track_to_queue(query)
        await ctx.send(cmd)
        print(f'{ctx.author.name} used "{str(ctx.message.content).strip()}" | {cmd}')


bot = Bot()
bot.run()