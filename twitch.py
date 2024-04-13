from twitchio.ext import commands
import spotify
import json


class Bot(commands.Bot):
    def __init__(self):
        with open('user_token.json', "r") as file:
            tokens = json.loads(file.read())
        ACCESS_TOKEN = tokens["token"]
        
        super().__init__(token = ACCESS_TOKEN, prefix = "!")

    async def event_ready(self):
        await super().join_channels(channels=[self.nick])
        print(f"Logged in as | {self.nick}")
        print(f"User ID is   | {self.user_id}")

    @commands.command(name="song", aliases=("playing", "np"))
    async def song_name(self, ctx: commands.Context):
        cmd = spotify.get_currently_playing()
        await ctx.send(cmd)
        print(f'{ctx.author.name} used "{str(ctx.message.content).strip()}" | {cmd}')

    @commands.command(name="sr", aliases=("queue", "q", "request", "play", "p"))
    async def song_request(self, ctx: commands.Context, *, query: str):
        cmd = spotify.add_track_to_queue(query)
        await ctx.send(cmd)
        print(f'{ctx.author.name} used "{str(ctx.message.content).strip()}" | {cmd}')


if __name__ == "__main__":
    ...