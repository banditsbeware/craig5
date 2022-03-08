from discord.ext import commands
import os
import json
import regex as re

# Import the wolfram language for computing our input
from wolfram import Wolfram
WF = Wolfram()

# Regular expression for determining the variable of an equation
# For example, "2x+3" is in terms of "x"
VR = re.compile( "^[a-df-z](?=[^a-z])|(?<=[^a-z])[a-df-z](?=[^a-z])|(?<=[^a-z])[a-df-z]$" )
def variable( s ):
  match = list( set( re.findall( VR, s ) ) )
  if len( match ) == 1: return match[0]
  return None

# Define this cog for implementation in the parent bot
class Calculus( commands.Cog, name='Calculus' ):
  def __init__( self, bot ):
    self.bot = bot

  # Formats user input for wolfram derivate function
  # assuming command format "derivative cos(x)"
  @commands.command( name="derivative", aliases=["d", "derive"] )
  async def derivative( self, ctx, *, args ):
    # Use regular expresseions to determine the terms of variable input by the user
    # For example, "2x+3" is in terms of "x"
    if args.find( ',' ) == -1:
      var = variable( args )

      # If no variable is identified, display a help message for the user
      if var is None: 
        await ctx.send( 'Usage: `>derivative f(x)` or `>derivative f(x,y,z), x`' )
        return 

      func = args
    # If a correctly formatted input is detected, compute it
    else:
      [ func, var ] = args.split( ',' )
    
    result = WF.evaluate( f'D[{ func }, { var }]' )
    await ctx.send( result )


  # Formats user input for wolfram integral function
  # assuming command format "integral 3x"
  @commands.command( name="integral", aliases=["i", "integrate"] )
  async def integral( self, ctx, *, args ):
    # Use regular expressions to determine the terms of variable input by the user
    # For example, "2x+3" is in terms of "x"
    if args.find( ',' ) == -1:
      var = variable( args )
      
      # If no variable is determined, display a help message to the user
      if var is None: 
        await ctx.send( 'Usage: `>integral f(x)` or `>integral f(x,y,z), x`' )
        return 

      func = args
    
    # If a valid command is detected, compute it
    else:
      [ func, var ] = args.split( ',' )

    result = WF.evaluate( f'Integrate[{ func }, { var }]' )
    await ctx.send( result )


  # Formats user input for wolfram limit function
  # assuming command format "limit x=5 as x approaches 75"
  @commands.command( name="limit", aliases=["l"] )
  async def limit( self, ctx, *, args ):    

    # If the user did not properly format their query, display a help message to the user
    if ',' not in args or '->' not in args:
      await ctx.send( 'Usage: `>limit f(x), x -> h`' )
      return
    # If valid input is detected, compute it
    else:
      [ func, var ] = args.split( ',' )

    result = WF.evaluate( f'Limit[{ func }, { var }]' )
    await ctx.send( result )

# Include this library as part of the parent bot
def setup( bot ):
    bot.add_cog( Calculus( bot ) )

# When this extension is unloaded from the parent bot, exit our Wolfram session
def teardown( bot ):
  logging.info( 'tearing down Calculus...' )
  WF.terminate()
