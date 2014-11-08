from __future__ import division,print_function
import sys,random,re
sys.dont_write_bytecode =True

from moead0 import *

def cmd(com='print(THE.MOEAD0._logo)'):
  if globals()["__name__"] == "__main__":
    if len(sys.argv) == 3:
      if sys.argv[1] == '--cmd':
        com = sys.argv[2] + '()'
      if len(sys.argv) == 4:
        com = sys.argv[2] + '(' + sys.argv[3] + ')'
    eval(com)

def _the():
  THAT(THE)

def _N():
  THE.LIB.buffer=32
  c1=N([x for x in xrange(10000)])
  print(sorted(c1.kept()))
  c2=N([r()+1 for _ in xrange(10000)])
  print(c2.lo,c2.hi,c2.norm(1.2),c2.dist(1.5,2))


cmd()
