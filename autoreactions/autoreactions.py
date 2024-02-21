import discord
import emoji
from discord.ext import commands
from discord.utils import get

class AutoReactions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.allowed_emojis = ['✅', '✍️', '✍🏻', '✍🏼', '✍🏽', '✍🏾', '✍🏿', '⌛']

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if str(payload.emoji) not in self.allowed_emojis:
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
            
            if message is None:
                return

            if message.author.id != self.bot.user.id:
                return
            
            currentChannelName = channel.name
            
            isEmoji = emoji.emoji_count(currentChannelName)
            if isEmoji > 0:
                currentChannelName = emoji.replace_emoji(currentChannelName, replace = '')

            newChannelName = f'{str(payload.emoji)}-{currentChannelName}'
            await channel.edit(name=newChannelName)

async def setup(bot):
    await bot.add_cog(AutoReactions(bot))
