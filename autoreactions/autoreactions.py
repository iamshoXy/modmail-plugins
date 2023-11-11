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
                print(message)

async def setup(bot):
    await bot.add_cog(AutoReactions(bot))
