from datetime import datetime

import discord
from discord.ext import commands

from core import checks
from core.models import PermissionLevel
from core.time import UserFriendlyTime

class TotalTickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @checks.has_permissions(PermissionLevel.ADMINISTRATOR)
    @commands.command()
    async def topsupporters(self, ctx, *, dt: UserFriendlyTime):
        """Sum total amount of numbers between the specified time period"""
        async with ctx.typing():
            date = discord.utils.utcnow() - (dt.dt - discord.utils.utcnow())

            logs = await self.bot.api.logs.find({"open": False}).to_list(None)
            closed_tickets = list(filter(lambda x: isinstance(x['closed_at'], str) and datetime.fromisoformat(x['closed_at']) > date, logs))

            em = discord.Embed(
                title='Closed Tickets',
                description=f'Total tickets closed: **{len(closed_tickets)}**',
                timestamp=date,
                color=0x7588da
            )
            em.set_footer(text='Since')
            await ctx.send(embed=em)

async def setup(bot):
    await bot.add_cog(TotalTickets(bot))