import os
from random import randint
from PIL import Image

pad = 10

name = f'img{ randint( 0, 9999999 ) }'
tex = f'{ name }.tex'
dvi = f'{ name }.dvi'
png = f'{ name }.png'

template = r'''
\documentclass[varwidth=true]{standalone}     
\usepackage{amsmath}           
\usepackage[utf8]{inputenc}

\begin{document} 
$$__EQN__$$
\end{document} 
'''

def texdoc( eqn ): 
  return template.replace( '__EQN__', eqn )

def texpng( eqn ):
  with open( tex, 'w' ) as f: f.write( texdoc( eqn ) )

  os.system( f'latex -interaction=batchmode { tex }' )
  os.system( f'dvipng -q* -D 300 -Q 5 { dvi } -o { png }' )
  os.system( f'rm -f *.tex *.aux *.dvi *.log' )

  im = Image.open( png )
  W, H = im.size
  res = Image.new( im.mode, ( W+2*pad, H+2*pad ), 'white' )
  res.paste( im, ( pad, pad ) )
  res.save( png )

  return png

