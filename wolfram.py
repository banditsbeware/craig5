import logging
import json
import regex as re
import subprocess

from wolframclient.evaluation import WolframLanguageSession
from wolframclient.language import wl, wlexpr

with open( './config.json', 'r' ) as f: config = json.load( f )

class Wolfram():
  def __init__( self ):
    self.session = WolframLanguageSession( config["wolfram_path"] )
    self.session.start()
    pass

  # def evaluate( self, expr ):
    # res = subprocess.check_output( ['wolframscript', '-code', f'\'{ expr }\''] ) 
    # return str( res, 'utf-8' )
    # pass

  def evaluate( self, expr ):
    result = self.session.evaluate( wlexpr( expr ) )
    return self.session.evaluate( f'ToString[ TeXForm[{ result }] ]' )

    # res = self.evaluate( expr )
    # res = self.evaluate( f'ToString[ TeXForm[ { res } ] ]' )
    print ( res )

    return res

if __name__ == '__main__':
  W = Wolfram()
  while 1:
    W.result( input('expr: ') )
