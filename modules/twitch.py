from . import spotify
from twitchio.ext import commands, routines
import json
from os.path import exists


class Bot(commands.Bot):
    def __init__(self):
        with open('user_token.json', "r") as file:
            tokens = json.loads(file.read())
        ACCESS_TOKEN = tokens["token"]
        
        super().__init__(token = ACCESS_TOKEN, prefix = "!")


    @routines.routine(minutes=5)
    async def keep_alive(self):
        spotify.auth()
        print(f"Keep alive pulse successful.")


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

        # can't gracefully exit this
        self.keep_alive.start()


    async def event_command_error(self, ctx: commands.Context, error: Exception):
        if isinstance(error, commands.CommandOnCooldown):
            cmd = f"Command on cooldown. Retry after {int(error.retry_after)} seconds."
            await ctx.send(cmd)
            print(f'{ctx.author.name} used "{str(ctx.message.content).strip()}" | {cmd}')


    @commands.command(name="song", aliases=("music", "nowplaying", "np", "playing"))
    async def song_name(self, ctx: commands.Context):
        cmd = spotify.get_currently_playing()
        await ctx.send(cmd)
        print(f'{ctx.author.name} used "{str(ctx.message.content).strip()}" | {cmd}')


    @commands.cooldown(rate=1, per=300, bucket=commands.Bucket.member)
    @commands.command(name="songrequest", aliases=("sr", "request", "r"))
    async def song_request(self, ctx: commands.Context, *, query: str):
        cmd = spotify.add_track_to_queue(query)
        await ctx.send(cmd)
        print(f'{ctx.author.name} used "{str(ctx.message.content).strip()}" | {cmd}')


    @commands.command(name="+songrequest", aliases=("+sr", "+request", "+r", "pls"))
    async def song_request_no_limit(self, ctx: commands.Context, *, query: str):
        if ctx.author.is_broadcaster or ctx.author.is_mod:
            cmd = spotify.add_track_to_queue(query)
            await ctx.send(cmd)
            print(f'{ctx.author.name} used "{str(ctx.message.content).strip()}" | {cmd}')
        else:
            cmd = "Command restricted to moderators only."
            await ctx.send(cmd)
            print(f'{ctx.author.name} used "{str(ctx.message.content).strip()}" | {cmd}')

    @commands.command(name="next", aliases=("n", "nextsong", "ns"))
    async def get_next(self, ctx: commands.Context, amount: int = 1):
        cmd = spotify.get_next_in_queue(amount)
        await ctx.send(cmd)
        print(f'{ctx.author.name} used "{str(ctx.message.content).strip()}" | {cmd}')


    @commands.command(name="queue", aliases=("q"))
    async def get_queue(self, ctx: commands.Context, amount: int = 5):
        cmd = spotify.get_next_in_queue(amount)
        await ctx.send(cmd)
        print(f'{ctx.author.name} used "{str(ctx.message.content).strip()}" | {cmd}')


    @commands.command(name="skip", aliases=("s"))
    async def skip_track(self, ctx: commands.Context):
        if ctx.author.is_broadcaster or ctx.author.is_mod:
            cmd = spotify.goto_next_track()
            await ctx.send(cmd)
            print(f'{ctx.author.name} used "{str(ctx.message.content).strip()}" | {cmd}')
        else:
            cmd = "Command restricted to moderators only."
            await ctx.send(cmd)
            print(f'{ctx.author.name} used "{str(ctx.message.content).strip()}" | {cmd}')


    @commands.command(name="previous", aliases=("prev", "rewind"))
    async def prev_track(self, ctx: commands.Context):
        if ctx.author.is_broadcaster or ctx.author.is_mod:
            cmd = spotify.goto_prev_track()
            await ctx.send(cmd)
            print(f'{ctx.author.name} used "{str(ctx.message.content).strip()}" | {cmd}')
        else:
            cmd = "Command restricted to moderators only."
            await ctx.send(cmd)
            print(f'{ctx.author.name} used "{str(ctx.message.content).strip()}" | {cmd}')


    @commands.command(name="pause", aliases=("stop"))
    async def pause_track(self, ctx: commands.Context):
        if ctx.author.is_broadcaster or ctx.author.is_mod:
            cmd = spotify.pause_current_track()
            await ctx.send(cmd)
            print(f'{ctx.author.name} used "{str(ctx.message.content).strip()}" | {cmd}')
        else:
            cmd = "Command restricted to moderators only."
            await ctx.send(cmd)
            print(f'{ctx.author.name} used "{str(ctx.message.content).strip()}" | {cmd}')


    @commands.command(name="resume", aliases=("play", "p"))
    async def resume_track(self, ctx: commands.Context):
        if ctx.author.is_broadcaster or ctx.author.is_mod:
            cmd = spotify.resume_current_track()
            await ctx.send(cmd)
            print(f'{ctx.author.name} used "{str(ctx.message.content).strip()}" | {cmd}')
        else:
            cmd = "Command restricted to moderators only."
            await ctx.send(cmd)
            print(f'{ctx.author.name} used "{str(ctx.message.content).strip()}" | {cmd}')


    @commands.command(name="volume", aliases=("vol", "v"))
    async def change_volume(self, ctx: commands.Context, volume: int):
        if ctx.author.is_broadcaster or ctx.author.is_mod:
            cmd = spotify.set_volume(volume)
            await ctx.send(cmd)
            print(f'{ctx.author.name} used "{str(ctx.message.content).strip()}" | {cmd}')
        else:
            cmd = "Command restricted to moderators only."
            await ctx.send(cmd)
            print(f'{ctx.author.name} used "{str(ctx.message.content).strip()}" | {cmd}')
