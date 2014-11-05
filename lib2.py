from __future__ import division,print_function
import sys, random,  datetime, time, re
sys.dont_write_bytecode =True

from base2 import *

@THE
def LIB(**d): return o(
    seed=1
    ).update(**d)

rand= random.random
seed= random.seed

print(THE().LIB)

def shuffle(lst): random.shuffle(lst); return lst

def say(*l):sys.stdout.write(', '.join(map(str,l)))

def sayln(*l): 
  say(*l), print("")
 
def g(lst,n=3):
  for col,val in enumerate(lst):
    if isinstance(val,float): val = round(val,n)
    lst[col] = val
  return lst

def printm(matrix):
  s = [[str(e) for e in row] for row in matrix]
  lens = [max(map(len, col)) for col in zip(*s)]
  fmt=' | '.join('{{:{}}}'.format(x) for x in lens)
  for row in [fmt.format(*row) for row in s]:
    print(row)

def study(f):
  def wrapper(*lst,**dic):
    doc   = f.__doc__ 
    args  = map(str,lst) + [('%s=%s' % (k,v)) 
                           for k,v in dic.items()]
    args  = ', '.join(args)
    call  = '\n### '+ f.__name__ +'('+args+') '
    if doc: doc= re.sub(r"\n[ \t]*","\n# ",doc)
    show = datetime.datetime.now().strftime
    print(call + ('#' * (50 - len(call))) + '#')
    print("#", show("%Y-%m-%d %H:%M:%S"))
    if doc:  print("#",doc)
    print("")
    t1 = time.time()
    f(*lst,**dic)          # run the function
    t2 = time.time() # show how long it took to run
    THOSE()
    print("\n# Runtime: %.3f secs" % (t2-t1))
  return wrapper

@study
def aa(a=1,b=2):
  """ere are som details we need to sort ouf
  as soon as we can"""
  i=1
  for j in xrange(100000): i += j
  print(j)


aa(b=40)
