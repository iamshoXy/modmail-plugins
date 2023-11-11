from discord.ext import commands

from core import checks

class AutoReactions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @checks.thread_only()
    @commands.Cog.listener()
    async def on_reaction_add(reaction, user):
        reaction_channel = reaction.message.channel
        messages = await reaction_channel.history(limit=1, oldest_first=True)
        print(messages)

def setup(bot):
    bot.add_cog(AutoReactions(bot))
