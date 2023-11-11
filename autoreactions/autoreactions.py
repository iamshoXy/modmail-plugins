import discord
from discord.ext import commands

from core import checks

class AutoReactions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.guild_id is None:
            return
    
        guild = await self.bot.fetch_guild(payload.guild_id)
        print(guild)
        member = guild.get_member(payload.user_id)
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
                    channelName = f'{str(payload.emoji)}-{channel.name}'
                    print(channelName)
                    await channel.edit(name=channelName)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.guild_id is None:
            return
        
        guild = await self.bot.fetch_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)

        if member is None or member.bot:
            return
        
        channel = self.bot.get_channel(payload.channel_id)
        if channel is None:
            return

        if isinstance(channel, discord.TextChannel) and channel.category_id == int(self.bot.config["main_category_id"]):
            async for message in channel.history(limit=1, oldest_first=True):  
                if message.id == payload.message_id:
                    channelName = channel.name.replace(str(payload.emoji), '').strip()
                    await channel.edit(name=channelName)

async def setup(bot):
    await bot.add_cog(AutoReactions(bot))
