from discord.ext import commands
import os
import json
import regex as re

from wolfram import Wolfram
WF = Wolfram()

VR = re.compile( "^[a-df-z](?=[^a-z])|(?<=[^a-z])[a-df-z](?=[^a-z])|(?<=[^a-z])[a-df-z]$" )
def variable( s ):
  match = list( set( re.findall( VR, s ) ) )
  if len( match ) == 1: return match[0]
  return None

class Calculus( commands.Cog, name='Calculus' ):
  def __init__( self, bot ):
    self.bot = bot

  # Formats user input for wolfram derivate function
  # assuming command format "derivative cos(x)"
  @commands.command( name="derivative", aliases=["d", "derive"] )
  async def derivative( self, ctx, *, args ):

    if args.find( ',' ) == -1:
      var = variable( args )

      if var is None: 
        await ctx.send( 'Usage: `>derivative f(x)` or `>derivative f(x,y,z), x`' )
        return 

      func = args

    else:
      [ func, var ] = args.split( ',' )

    result = WF.evaluate( f'D[{ func }, { var }]' )
    await ctx.send( wolf_to_tex( result ) )


  # Formats user input for wolfram integral function
  # assuming command format "integral 3x"
  @commands.command( name="integral", aliases=["i", "integrate"] )
  async def integral( self, ctx, *, args ):

    if args.find( ',' ) == -1:
      var = variable( args )

      if var is None: 
        await ctx.send( 'Usage: `>integral f(x)` or `>integral f(x,y,z), x`' )
        return 

      func = args

    else:
      [ func, var ] = args.split( ',' )

    result = WF.evaluate( f'Integrate[{ func }, { var }]' )
    await ctx.send( wolf_to_tex( result ) )


  # Formats user input for wolfram limit function
  # assuming command format "limit x=5 as x approaches 75"
  @commands.command( name="limit" )
  async def limit( self, ctx, *, args ):    

    if ',' not in args or '->' not in args:
      await ctx.send( 'Usage: `>limit f(x), x -> h`' )
      return
    else:
      [ func, var ] = args.split( ',' )

    result = WF.evaluate( f'Limit[{ func }, { var }]' )
    await ctx.send( wolf_to_tex( result ) )


def setup( bot ):
    bot.add_cog( Calculus( bot ) )

def teardown( bot ):
  logging.info( 'tearing down Calculus...' )
  WF.terminate()
