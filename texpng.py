import os
from random import randint

name = f'texpng{ randint( 0, 9999999 ) }'
tex = f'{ name }.tex'
dvi = f'{ name }.dvi'
png = f'{ name }.png'

template = r'''
\documentclass[varwidth=true]{standalone}     
\usepackage{amsmath}           
\usepackage{color}
\usepackage[usenames,dvipsnames,svgnames,table]{xcolor}
\usepackage[utf8]{inputenc}

\definecolor{dstext}{HTML}{FFFFFF}
\definecolor{dsbackground}{HTML}{36393F}

\begin{document} 
\color{dstext}
\pagecolor{dsbackground}
\begin{align*}
__EQN__ 
\end{align*}
\end{document} 
'''

def texdoc( eqn ): 
  return template.replace( '__EQN__', eqn )


def texpng( eqn ):

  with open( tex, 'w' ) as f: f.write( texdoc( eqn ) )

# os.system( f'rm { png }' )
  os.system( f'latex -interaction=batchmode { tex }' )
# os.system( f'dvipng -q* -D 300 -Q 5 -T tight { dvi } -o { png }' )
  os.system( f'dvipng -q* -D 300 -Q 5 { dvi } -o { png }' )
  os.system( f'rm -f *.tex *.aux *.dvi *.log' )

  return png

