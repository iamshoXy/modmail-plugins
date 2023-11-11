import discord
from discord.ext import commands

from core import checks

class AutoReactions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.member.bot:
            return
        
        channel = await self.get_channel(payload.channel_id)

        if isinstance(channel, discord.TextChannel) and channel.category_id == int(self.bot.config["main_category_id"]):
            async for message in channel.history(limit=1, oldest_first=True):
                if message.id == payload.message_id:
                    channelName = payload.emoji + "-" + channel.name
                    await channel.edit(name=channelName)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.member.bot:
            return
        
        channel = await self.get_channel(payload.channel_id)

        if isinstance(channel, discord.TextChannel) and channel.category_id == int(self.bot.config["main_category_id"]):
            async for message in channel.history(limit=1, oldest_first=True):  
                if message.id == payload.message_id:
                    channelName = channel.name.replace(payload.emoji, '').strip()
                    await channel.edit(name=channelName)

async def setup(bot):
    await bot.add_cog(AutoReactions(bot))
