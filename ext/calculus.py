
from discord.ext import commands
import os
import json

from wolframclient.evaluation import WolframLanguageSession
from wolframclient.language import wl, wlexpr

with open('./config.json', 'r') as f:
  config = json.load(f)


import regex as re
def wolf_to_tex(expr):
  expr = re.sub('Global`', '', expr)
  return expr


class Calculus(commands.Cog, name='Calculus'):
  def __init__(self, bot):
    self.bot = bot
    self.session = WolframLanguageSession(config["wolfram_path"])

  def eval(self, expr):
    return str( self.session.evaluate( wlexpr( expr ) ) )
    
  # Formats user input for wolfram derivate function
  # assuming command format "derivative cos(x)"
  @commands.command(name="derivative")
  async def derivative(self, ctx, args):
    await ctx.send(f'D[{args}, x]')

  # Formats user input for wolfram integral function
  # assuming command format "integral 3x"
  @commands.command(name="integral", aliases=["i", "integrate"])
  async def integral(self, ctx, *, args):
    if args.find(',') == -1:
      await ctx.send('Usage: `>integral f(x), x`')
    else:
      [func, var] = args.split(',')

    result = self.eval( f'Integrate[{ func }, { var }]' )
    await ctx.send( wolf_to_tex( result ) )

  # Formats user input for wolfram limit function
  # assuming command format "limit x=5 as x approaches 75"
  @commands.command(name="limit")
  async def limit(self, ctx, *, args):    
    msg = args.split(" ");
    await ctx.send(f'Integrate[{msg[0]}, {msg[2]}->{msg[4]}]')

def setup(bot):
    bot.add_cog(Calculus(bot))
