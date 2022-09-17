# Taken from https://github.com/interactions-py/lavalink/tree/main/examples

import interactions
from interactions.ext.lavalink import VoiceClient, VoiceState
from lavalink import AudioTrack

import os

class Music(interactions.Extension):
    def __init__(self, client):
        self.client: VoiceClient = client

    @interactions.extension_listener()
    async def on_start(self):
        self.client.lavalink_client.add_node(os.getenv("LAVALINK_SERVER_ADDRESS"), os.getenv("LAVALINK_SERVER_PORT"), os.getenv("LAVALINK_SERVER_PASSWORD"), "eu")

    @interactions.extension_listener()
    async def on_voice_state_update(self, before: VoiceState, after: VoiceState):
        """
        Disconnect if bot is alone
        """
        if before and not after.joined:
            voice_states = self.client.get_channel_voice_states(before.channel_id)
            if len(voice_states) == 1 and voice_states[0].user_id == self.client.me.id:
                await self.client.disconnect(before.guild_id)

    @interactions.extension_command(
        name="play",
        description="Play music in a VC (you need to be in VC to do this, obviously)"
    )
    @interactions.option()
    async def play(self, ctx: interactions.CommandContext, query: str):
        await ctx.defer()

        player = await self.client.connect(ctx.author.voice.guild_id, ctx.author.voice.channel_id)

        results = await player.node.get_tracks(f"ytsearch:{query}")
        track = AudioTrack(results["tracks"][0], int(ctx.author.id))
        player.add(requester=int(ctx.author.id), track=track)
        await player.play()

        await ctx.send(f"Now playing: `{track.title}`")

    @interactions.extension_command(
        name="pause",
        description="Pause playback of music"
    )
    async def pause(self, ctx):
        await ctx.defer()

        player = await self.client.connect(ctx.author.voice.guild_id, ctx.author.voice.channel_id)
        await player.set_pause(True)

        await ctx.send("Paused")

    @interactions.extension_command(
        name="resume",
        description="Resume playback"
    )
    async def resume(self, ctx):
        await ctx.defer()

        player = await self.client.connect(ctx.author.voice.guild_id, ctx.author.voice.channel_id)
        await player.set_pause(False)

        await ctx.send("Resuming playback")

    @interactions.extension_command(
        name="leave",
        description="When you're done, run this command to make SquidBOT leave the VC."
    )
    async def leave(self, ctx: interactions.CommandContext):
        await self.client.disconnect(ctx.guild_id)
        await ctx.send("Left VC")

    @interactions.extension_command(
        name="moveto",
        description="Move SquidBOT to a different listening VC"
    )
    @interactions.option(channel_types=[interactions.ChannelType.GUILD_VOICE])
    async def move_to(self, ctx: interactions.CommandContext, channel: interactions.Channel):
        await self.client.connect(ctx.guild_id, channel.id)
        await ctx.send("Moved VCs")

    @interactions.extension_command(
        name="stop",
        description="Stops playback (THIS IS NOT THE SAME AS PAUSE)"
    )
    async def stop(self, ctx):
        await ctx.defer()

        player = await self.client.connect(ctx.author.voice.guild_id, ctx.author.voice.channel_id)
        await player.stop()

        await ctx.send("Stopped playback")


def setup(client):
    Music(client)
