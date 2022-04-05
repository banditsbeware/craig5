from discord.ext import commands
from discord import File
import os
import json
import regex as re

# Import the wolfram language for computing our input
from wolfram import Wolfram
WF = Wolfram()

from texpng import *

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
    png = File( texpng( result ) )
    await ctx.send( file=png )


  # Formats user input for wolfram integral function
  # assuming command format "integral 3x"
  @commands.command( name="integral", aliases=["I", "i", "integrate"] )
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
    png = File( texpng( result ) )
    await ctx.send( file=png )


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
    png = File( texpng( result ) )
    await ctx.send( file=png )
    

  # Formats user input for the Wolfram Total Derivative function
  # Assumes input format "totalderivative 3x x"
  @commands.command( name = "totalderivative", aliases=["dt"] )
  async def total_derivative( self, ctx, *, args ):
    # use regular expressions to determine the terms of the variable input by the user
    # for example, "2x+3" is in terms of "x"
    if args.find( ',' ) == -1:
      var = variable( args )

      # if no variable is identified, display a help message for the user
      if var is none:
          await ctx.send( 'usage: `>dt f(x)` or `>dt f(x,y,z), x`' )
          return

      func = args
    # if a correctly formatted input is detected, compute it
    else:
      [ func, var ] = args.split( ',' )

    result = WF.evaluate( f'dt[{ func }, { var }]' )
    png = File( texpng( result ) )
    await ctx.send( file=png )


  # Formats user input for the Wolfram Max Limit function
  # Assumes input "maxl 3x, x -> 3"
  @commands.command( name="maxlimit", aliases=["maxl"] )
  async def max_limit( self, ctx, *, args ):
    # Use regular expressions to determine the terms of variable input by the user
    # For example, "2x+3" is in terms of "x"
    if args.find( ',' ) == -1:
      var = variable( args )
      
      # If no variable is determined, display a help message to the user
      if var is None: 
        await ctx.send( 'Usage: `>maxlimit f(x), x -> h`' )
        return 

      func = args
    
    # If a valid command is detected, compute it
    else:
      [ func, var ] = args.split( ',' )

    result = WF.evaluate( f'MaxLimit[{ func }, { var }]' )
    png = File( texpng( result ) )
    await ctx.send( file=png )


  # Formats user input for the Wolfram Min Limit function
  # Assumes input "minl 3x, x -> 3"
  @commands.command( name="minlimit", aliases=["minl", "minimuml", "minimumlimit"] )
  async def min_limit( self, ctx, *, args ):
    # Use regular expressions to determine the terms of variable input by the user
    # For example, "2x+3" is in terms of "x"
    if args.find( ',' ) == -1:
      var = variable( args )
      
      # If no variable is determined, display a help message to the user
      if var is None: 
        await ctx.send( 'Usage: `>minlimit f(x), x -> h`' )
        return 

      func = args
    
    # If a valid command is detected, compute it
    else:
      [ func, var ] = args.split( ',' )

    result = WF.evaluate( f'MinLimit[{ func }, { var }]' )
    png = File( texpng( result ) )
    await ctx.send( file=png )


# Include this library as part of the parent bot
def setup( bot ):
    bot.add_cog( Calculus( bot ) )

# When this extension is unloaded from the parent bot, exit our Wolfram session
def teardown( bot ):
  logging.info( 'tearing down Calculus...' )
  WF.terminate()
