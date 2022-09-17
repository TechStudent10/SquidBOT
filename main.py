import interactions
# from interactions.ext.lavalink import VoiceClient, VoiceState

import firebase_admin
from firebase_admin import db

import random, os

from dotenv import load_dotenv
load_dotenv()

presence_string_list = [
    "SquidKIDS",
    "moderators",
    "slash commands",
    "idk",
    "/help, wait that doesn't exist",
    "developers",
    "open source"
]

cred_obj = firebase_admin.credentials.Certificate(os.getenv("FIREBASE_CREDS_FILE"))
default_app = firebase_admin.initialize_app(cred_obj, {
    "databaseURL": os.getenv("FIREBASE_DATABASE_URL")
})

root = db.reference("/")
warns = db.reference("/warns")

bot = interactions.Client(token=os.getenv("TOKEN"), intents=interactions.Intents.DEFAULT | interactions.Intents.GUILD_MEMBERS)
LOGS_CHANNEL = 1016429819094913044

@bot.event
async def on_start():
    print("Splash! I'm ready to do your bidding.")
    await bot.change_presence(
        interactions.ClientPresence(
            status=interactions.StatusType.ONLINE,
            activities=[
            interactions.PresenceActivity(name=random.choice(presence_string_list), type=interactions.PresenceActivityType.WATCHING)
            ]
        )
    )

@bot.event
async def on_command_error(ctx, traceback):
    logs_channel = await interactions.get(bot, interactions.Channel, object_id=LOGS_CHANNEL)
    await logs_channel.send(f"""Error occured in #{ctx.channel}.
```python
{traceback}
```""")

@bot.event
async def on_guild_member_add(member):
    await member.send("Welcome to SquidKIDS, the fan server for Geometry Dash YouTuber Squidel. Talk with other members about Squidel's channel, Geometry Dash events, and basically anything. Thank you for joining!")

@bot.command(
    name="ping",
    description="PONG!"
)
async def ping(ctx):
    await ctx.send("Pong!")

@bot.command(
    name="squid",
    description="squidel"
)
async def squid(ctx):
    await ctx.send("#1: Squidel")

@bot.command(
    name="social",
    description="List of all Squidel's social media!"
)
async def social(ctx):
    await ctx.send("""
YouTube: https://www.youtube.com/channel/UCAMedxAMmz3UjmV3tv_a-LQ
""")

@bot.command(
    name="profile",
    description="Shows info about a server member (warns, date created, date joined, etc.)"
)
@interactions.option("Member to show info about")
async def profile(ctx, member: interactions.User):
    member_name = member.name
    member_pfp = member.get_avatar_url(ctx.guild.id)

    warns_num = 0
    bans_num = 0

    warns_dict = warns.get()
    if member.name not in warns_dict:
        warns_num = 0
    else:
        warns_num = len(warns_dict[member.name])

    embed = interactions.Embed(
        title=f"{member_name}"
    )
    embed.set_image(member_pfp)
    embed.add_field("Warns", warns_num, True)
    embed.add_field("Join Date", member.joined_at.isoformat(), True)

    await ctx.send(embeds=embed)

bot.load("exts.moderation")
# bot.load("exts.music")
# Music bot offline until I get hosting for Lavalink
bot.start()
