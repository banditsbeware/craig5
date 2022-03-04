from discord.ext import commands
import os

# owner commands
class Owner(commands.Cog, name='Owner'):
  def __init__(self, bot):
    self.bot = bot
      
  # unloads an extension 
  @commands.command(name="unload")
  @commands.is_owner() 
  async def unload_cmd(self, ctx, ext):
    self.bot.unload_extension(f'ext.{ext}')
    await ctx.send(f'unloaded **{ext}** ')
  
  # loads an extension
  @commands.command(name="load")
  @commands.is_owner() 
  async def load_cmd(self, ctx):
    for f in os.listdir('./ext'):
      if f.endswith('.py'):
        self.bot.load_extension(f'ext.{f[:-3]}')

    extstr = ', '.join( [ e[4:] for e in self.bot.extensions ] )
    await ctx.send(f'extensions loaded:\n{extstr}')

  # reloads an extension
  @commands.command(name="reload")
  @commands.is_owner()
  async def reload_cmd(self, ctx, ext):
    self.bot.unload_extension(f'ext.{ext}')
    self.bot.load_extension(f'ext.{ext}')
    await ctx.send(f'reloaded **{ext}** ')

  # reloads all extensions
  @commands.command(name="reloadall")
  @commands.is_owner()
  async def reload_all(self, ctx):
    extstr = ', '.join( [ e[4:] for e in self.bot.extensions ] )
    for ext in list(self.bot.extensions):
      self.bot.reload_extension(ext)
      
    await ctx.send(f'extensions reloaded:\n{extstr}')
  
  # shutdown the bot via command
  @commands.command(name="shutdown")
  @commands.is_owner()
  async def shutdown_cmd(self, ctx):
    await ctx.send('goodbye（︶^︶）')
    await ctx.bot.logout()


def setup(bot):
  bot.add_cog(Owner(bot))
