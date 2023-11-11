import discord
from discord.ext import commands

from core import checks

class AutoReactions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        reaction_channel = reaction.message.channel

        if isinstance(reaction_channel, discord.TextChannel) and reaction_channel.category_id == int(self.bot.config["main_category_id"]):
            async for message in reaction_channel.history(limit=1, oldest_first=True):
                if message.id == reaction.message.id:
                    channelName = reaction.emoji + "-" + reaction_channel.name
                    print(channelName)
                    await reaction_channel.edit(name=channelName)

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        reaction_channel = reaction.message.channel

        if isinstance(reaction_channel, discord.TextChannel) and reaction_channel.category_id == int(self.bot.config["main_category_id"]):
            async for message in reaction_channel.history(limit=1, oldest_first=True):  
                if message.id == reaction.message.id:
                    channelName = reaction_channel.name.replace(reaction.emoji, '').strip()
                    await reaction_channel.edit(name=channelName)

async def setup(bot):
    await bot.add_cog(AutoReactions(bot))
