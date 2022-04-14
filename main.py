import discord
import logging
import atexit
import json
import os
from discord.ext import commands

logging.basicConfig( level=logging.DEBUG )

with open( './config.json', 'r' ) as f: config = json.load( f )

__version__ = '1.0'

intents = discord.Intents.default()

bot = commands.Bot( command_prefix='>', case_sensitive=True, intents=intents )
bot.remove_command( 'help' )

for f in os.listdir( './ext' ):
  if f.endswith( '.py' ):
    bot.load_extension( f'ext.{f[:-3]}' )
    logging.info( f'ext.{f[:-3]} loaded')

@bot.event
async def on_ready():
  bot.App = await bot.application_info()
  logging.info( f'Logged in as     {bot.user.name}' )
  logging.info( f'Bot ID:          {bot.user.id}' )
  logging.info( f'Discord version: {discord.__version__}' )
  logging.info( f'Bot version:     {__version__}' )
  logging.info( f'Owner:           {bot.App.owner}' )

bot.run( config['discord_token'] )
