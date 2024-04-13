from twitchio.ext import commands
import spotify
import json
from os.path import exists


class Bot(commands.Bot):
    def __init__(self):
        with open('user_token.json', "r") as file:
            tokens = json.loads(file.read())
        ACCESS_TOKEN = tokens["token"]
        
        super().__init__(token = ACCESS_TOKEN, prefix = "!")


    async def event_ready(self):
        self.channels = [self.nick]

        if exists("channels.txt"):
            with open("channels.txt", "r") as file:
                for channel in file.readlines():
                    self.channels.append(channel.strip())
            self.channels = list(set(map(str.lower, self.channels)))
    
        await super().join_channels(channels=self.channels)
        print(f"Twitch username | {self.nick}")
        print(f"User ID is      | {self.user_id}")
        print(f"Spotify name    | {spotify.get_username()}")
        print(f"Joined channels | {self.channels}")


    async def event_command_error(self, ctx: commands.Context, error: Exception):
        if isinstance(error, commands.CommandOnCooldown):
            cmd = f"Command on cooldown. Retry after {int(error.retry_after)} seconds."
            await ctx.send(cmd)
            print(f'{ctx.author.name} used "{str(ctx.message.content).strip()}" | {cmd}')


    @commands.command(name="song", aliases=("music", "playing", "np"))
    async def song_name(self, ctx: commands.Context):
        cmd = spotify.get_currently_playing()
        await ctx.send(cmd)
        print(f'{ctx.author.name} used "{str(ctx.message.content).strip()}" | {cmd}')


    @commands.cooldown(rate=1, per=300, bucket=commands.Bucket.member)
    @commands.command(name="sr", aliases=("queue", "q", "request", "r", "play", "p"))
    async def song_request(self, ctx: commands.Context, *, query: str):
        cmd = spotify.add_track_to_queue(query)
        await ctx.send(cmd)
        print(f'{ctx.author.name} used "{str(ctx.message.content).strip()}" | {cmd}')
