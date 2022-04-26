from discord.ext import commands
from discord import File
import os
import json

class Function:
  def __init__(self, f_name, help_message, command):
    self.f_name = f_name
    self.help_message = help_message
    self.command = command

# This was written in an attempt to make the code easy to expand as more commands are implemented.
# To add a new help message, copy and paste the append line. the first parameter is the function name,
# the second is the help message
# the third is an example of the command
functions = []
functions.append( Function('limit', 'Input formatted as >limit function, variable->value. "limit" can also be abbreviated to "l"', '>limit 3x, x->32') )
functions.append( Function('derivative', 'Input formatted as >derivative function. "derivative" can also be abbreviated to "d"', '>derivative cos(x)') )
functions.append( Function('integral', 'Input formatted as >integral function. For example, "integral" can also be abbreviated to "i"', '>integral cos(x)') )
functions.append( Function('totalderivative', 'Input formatted as >totalderivative function. "totalderivative" can also be abbreviated to "dt"', '>totalderivative cos(x)') )
functions.append( Function('maxlimit', 'Input formatted as >maxlimit function or alternatively >maxlimit function variable->value. "maxlimit" can also be abbreviated to "maxl"',' >maxlimit 3x') )
functions.append( Function('minlimit', 'Input formatted as >minlimit function or alternatively >minlimit function as variable approaches value. "minlimit" can also be abbreviated to "minl"', '>minlimit 3x') )

# Define this cog for implementation in the parent bot
class Help( commands.Cog, name='Help' ):
  def __init__( self, bot ):
    self.bot = bot

  # Formats user input for wolfram derivate function
  # assuming command format "derivative cos(x)"
  @commands.command( name="help", aliases=["h"] )
  async def help( self, ctx, *, args='' ):
    # Use regular expresseions to determine the terms of variable input by the user
    # For example, "2x+3" is in terms of "x"
    # if args.find( ' ' ) == -1:
    if len(args) == 0:
      await ctx.send( 'For a list of commands, try >commands. For help with a specific command, try >help command_name ')

    else:
      # help, func ] = args.split( ' ' )
      # some random stack overflow article said this is how you format a python switch statement 
      # but if not we just swap it with a cascading if
      func = args.split()
      return_msg = ''
      for y in func:
        for x in functions:
          if y  == x.f_name:
            return_msg += '**' + x.f_name + '** - ' + x.help_message + '```' + x.command + '```\n' 
      if return_msg == '':
        return_msg = 'Command not found '+', '.join(func)
      await ctx.send ( return_msg )
      # Attempt at making the code expandable so we never have to actually update this function, just the list       
      
  @commands.command( name="commands", aliases=["c"] )
  async def commands( self, ctx, *, args='' ):
    # this might break if we try to send too much text in one message
    message = ''
    for x in functions:
        message += '**' + x.f_name + '** - ' + x.help_message + '```' + x.command + '```\n'
    if message == '':
      message = 'No commands available'
    await ctx.send( message )

# Include this library as part of the parent bot
def setup( bot ):
    bot.add_cog( Help( bot ) )

# When this extension is unloaded from the parent bot, exit our Wolfram session
def teardown( bot ):
  logging.info( 'tearing down Help...' )
