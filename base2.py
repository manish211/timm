from __future__ import division,print_function
import sys
sys.dont_write_bytecode =True

def fun(x): 
  return x.__class__.__name__ == 'function'

class o:
  def __init__(i,**d): i.update(**d)
  def update(i,**d): i.dict().update(**d); return i
  def dict(i): return i.__dict__
  def __repr__(i)   : 
    def name(x): return x.__name__ if fun(x) else x
    d    = i.dict()
    show = [':%s=%s' % (k,name(d[k])) 
            for k in sorted(d.keys() ) 
            if k[0] is not "_"]
    return '{'+' '.join(show)+'}'

def THE(f=None,cache=o()):
  "To keep the options, cache their last setting."
  if not f: return cache
  cached = cache.dict()
  if not f.__name__ in cached: cached[f.__name__] = f()
  def wrapper(*l,**d):
    tmp = cached[f.__name__] = f(*l,**d)
    return tmp
  return wrapper

def THOSE():
  d1 = THE().dict()
  for key1 in sorted(d1.keys()):
    print('%s =' % key1)
    sub = d1[key1]
    if isinstance(sub,o):
      d2 = sub.dict()
      for key2 in sorted(d2.keys()):
        print('\t%s = %s' % (key2, d2[key2]))
    else:
      print('\t$s = %s' % (key1, sub))
