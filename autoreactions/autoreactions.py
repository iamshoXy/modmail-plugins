import discord
from discord.ext import commands
from discord.utils import get

from core import checks

class AutoReactions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.guild_id is None:
            return

        member = payload.member
        if member is None or member.bot:
            return
        
        channel = self.bot.get_channel(payload.channel_id)
        if channel is None:
            return

        if isinstance(channel, discord.TextChannel) and channel.category_id == int(self.bot.config["main_category_id"]):
            async for message in channel.history(limit=1, oldest_first=True):
                if message.id == payload.message_id:
                    channelName = f'{str(payload.emoji)}-{channel.name}'
                    print(channelName)
                    await channel.edit(name=channelName)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.guild_id is None:
            return
        
        guild = self.bot.get_channel(payload.guild_id)
        print(guild)
        member = get(guild.members, id=payload.user_id)
        print(member)
        if member is None or member.bot:
            return
        
        channel = self.bot.get_channel(payload.channel_id)
        print(channel)
        if channel is None:
            return

        if isinstance(channel, discord.TextChannel) and channel.category_id == int(self.bot.config["main_category_id"]):
            async for message in channel.history(limit=1, oldest_first=True):  
                if message.id == payload.message_id:
                    channelName = channel.name.replace(str(payload.emoji), '').strip()
                    await channel.edit(name=channelName)

async def setup(bot):
    await bot.add_cog(AutoReactions(bot))
