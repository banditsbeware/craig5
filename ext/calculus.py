
from discord.ext import commands
import os
# INCLUDE THE WOLFRAM LIBRARY

# owner commands
class Calculus(commands.Cog, name='Calculus'):
  def __init__(self, bot):
    self.bot = bot
    
  # Formats user input for wolfram derivate function
  # assuming command format "derivative cos(x)"
  @commands.command(name="derivative")
  async def derivative(self, ctx, args):
    await ctx.send(f'D[{args}, x]')

  # Formats user input for wolfram integral function
  # assuming command format "integral 3x"
  @commands.command(name="integral")
  async def integral(self, ctx, args):
    await ctx.send(f'Integrate[{args}, x]')

  # Formats user input for wolfram limit function
  # assuming command format "limit x=5 as x approaches 75"
  @commands.command(name="limit")
  async def limit(self, ctx, *, args):    
    msg = args.split(" ");
    await ctx.send(f'Integrate[{msg[0]}, {msg[2]}->{msg[4]}]')

def setup(bot):
    bot.add_cog(Calculus(bot))

