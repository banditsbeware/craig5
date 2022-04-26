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

# interpret user input
def input_intr( s ):
  
  pass
  


# Define this cog for implementation in the parent bot
class Arithmetic( commands.Cog, name='Arithmetic' ):
  def __init__( self, bot ):
    self.bot = bot

  '''
  @bot.event
  async def on_message(message):
      if message.author == bot.user:
          return
      content = message.content
      regex = "" 
      if content[0] != '>' 
  '''


# Include this library as part of the parent bot
def setup( bot ):
    bot.add_cog( Arithmetic( bot ) )

# When this extension is unloaded from the parent bot, exit our Wolfram session
def teardown( bot ):
  logging.info( 'tearing down Arithmetic...' )
  WF.terminate()
