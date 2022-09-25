import interactions
import firebase_admin
from firebase_admin import db
import os

cred_obj = firebase_admin.credentials.Certificate(os.getenv("FIREBASE_CREDS_FILE"))
default_app = firebase_admin.initialize_app(cred_obj, {
    "databaseURL": os.getenv("FIREBASE_DATABASE_URL")
}, "mains")

root = db.reference("/")
warns = db.reference("/warns")

STAFF_ID = os.getenv("STAFF_ID")
MUTED_ID = os.getenv("MUTED_ID")

class Moderation(interactions.Extension):
    def __init__(self, client):
        self.bot: VoiceClient = client

    @interactions.extension_command(
        name="ban",
        description="Bans the user from the server"
    )
    @interactions.option("User to be banned")
    @interactions.option("Reason for the ban")
    async def perm_ban(self, ctx, user: interactions.User, reason: str):
        author = ctx.author
        if not STAFF_ID in author.roles:
            await ctx.send("You do not have permissions to do this.")
            return

        guild = ctx.guild
        await user.send(f"You have been banned from SquidKIDS for the following reason: {reason}")
        await guild.ban(member_id=user, reason=reason)

        embed = interactions.Embed(description=f"Successfully banned `{user}`. \nReason: {reason}")
        await ctx.send(embeds=embed)

    @interactions.extension_command(
        name="unban",
        description="Unbans a member from the server",
    )
    @interactions.option("User to be unbanned")
    async def unban(self, ctx, user: interactions.User):
        author = ctx.author
        if not STAFF_ID in author.roles:
            await ctx.send("You do not have permissions to do this.")
            return

        guild = ctx.guild
        await guild.remove_ban(user)

        embed = interactions.Embed(description=f"Successfully unbanned `{user}`.")
        await ctx.send(embeds=embed)

    @interactions.extension_command(
        name="kick",
        description="Kick a member from the server"
    )
    @interactions.option("Member to be kicked")
    @interactions.option("Reason for the kick")
    async def kick(self, ctx, user: interactions.User, reason: str):
        author = ctx.author
        if not STAFF_ID in author.roles:
            await ctx.send("You do not have permissions to do this.")
            return

        guild = ctx.guild
        await user.send(f"You have been kicked from SquidKIDS for the following reason: {reason}")
        await guild.kick(member_id=user, reason=reason)

        embed = interactions.Embed(description=f"Successfully kicked `{user}`. \nReason: {reason}")
        await ctx.send(embeds=embed)

    @interactions.extension_command(
        name="warn",
        description="Warn a member"
    )
    @interactions.option("Member to be warned")
    @interactions.option("Reason for the warn")
    async def warn(self, ctx, user: interactions.User, reason: str):
        author = ctx.author
        if not STAFF_ID in author.roles:
            await ctx.send("You do not have permissions to do this.")
            return

        if user.name == "SquidBOT":
            await ctx.send("What? You want to warn me? That... makes no sense. I did nothing wrong! Like seriously!")
            return

        warns_dict = warns.get()
        if user.name not in warns_dict:
            warns.child(user.name).set({})

        warns.child(user.name).push({
            "reason": reason
        })

        embed = interactions.Embed(description=f"Warned `{user}`.")
        await ctx.send(embeds=embed)

    @interactions.extension_command(
        name="mute",
        description="Mute a member"
    )
    @interactions.option("Member to be muted")
    async def mute(self, ctx, member: interactions.User):
        author = ctx.author
        if not STAFF_ID in author.roles:
            await ctx.send("You do not have permissions to do this.")
            return

        if member.name == "SquidBOT":
            await ctx.send("imagine trying to mute me, thats crazy")
            return

        await member.add_role(MUTED_ID, ctx.guild.id)
        embed = interactions.Embed(description=f"Muted {member}")
        await ctx.send(embeds=embed)

    @interactions.extension_command(
        name="unmute",
        description="Unmute a member"
    )
    @interactions.option("Member to be unmuted")
    async def unmute(self, ctx, member: interactions.User):
        author = ctx.author
        if not STAFF_ID in author.roles:
            await ctx.send("You do not have permissions to do this.")
            return

        if member.name == "SquidBOT":
            await ctx.send("i can already talk bro")
            return

        await member.remove_role(MUTED_ID, ctx.guild.id)
        embed = interactions.Embed(description=f"Unmuted {member}")
        await ctx.send(embeds=embed)

def setup(client):
    Moderation(client)
