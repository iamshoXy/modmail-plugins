import discord
from discord.ext import commands
from discord.utils import get

class AutoReactions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if str(payload.emoji) != '✅':
            return
        
        if payload.guild_id is None:
            return

        member = payload.member
        if member is None or member.bot:
            return
        
        channel = self.bot.get_channel(payload.channel_id)
        if channel is None:
            return

        if isinstance(channel, discord.TextChannel) and channel.category_id == int(self.bot.config["main_category_id"]):
            message = await channel.fetch_message(payload.message_id)
            print(message)
            if message is None:
                return

            if message.author.id != '1070726122192523385':
                return
            
            channelName = f'{str(payload.emoji)}-{channel.name}'
            await channel.edit(name=channelName)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if str(payload.emoji) != '✅':
            return
        
        if payload.guild_id is None:
            return
        
        guild = self.bot.get_guild(payload.guild_id)
        if guild is None:
            return
        
        member = get(guild.members, id=payload.user_id)
        if member is None or member.bot:
            return
        
        channel = self.bot.get_channel(payload.channel_id)
        if channel is None:
            return

        if isinstance(channel, discord.TextChannel) and channel.category_id == int(self.bot.config["main_category_id"]):
            message = await channel.fetch_message(payload.message_id)
            if message is None:
                return
            
            if message.author.id != '1070726122192523385':
                return
            
            channelName = channel.name.replace(str(payload.emoji), '').strip()
            await channel.edit(name=channelName)

async def setup(bot):
    await bot.add_cog(AutoReactions(bot))
