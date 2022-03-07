import atexit
import logging
import json
import regex as re

from wolframclient.evaluation import WolframLanguageSession
from wolframclient.language import wl, wlexpr

with open( './config.json', 'r' ) as f: config = json.load( f )

class Wolfram():
  def __init__( self ):
    self.session = WolframLanguageSession( config["wolfram_path"] )
    self.session.start()
    atexit.register( self.terminate )

  def evaluate( self, expr ):
    result = str( self.session.evaluate( wlexpr( expr ) ) )
    result = re.sub( 'Global1', '', result )
    return result

  def terminate( self ):
    logging.info( 'terminating wolfram session' )
    self.session.stop()