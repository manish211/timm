from __future__ import division,print_function
import sys
sys.dont_write_bytecode =True

def the(f=None,cache={}):
  "To keep the options, cache their last setting."
  if not f: return cache
  if not f.__name__ in cache: cache[f.__name__] = f()
  def wrapper(*l,**d):
    tmp = cache[f.__name__] = f(*l,**d)
    return tmp
  return wrapper

def fun(x): 
  return x.__class__.__name__ == 'function'

class o:
  def __init__(i,**d): i.update(**d)
  def update(i,**d): 
    i.__dict__.update(**d); return i
  def __repr__(i)   : 
    def name(x): return x.__name__ if fun(x) else x
    d    = i.__dict__
    show = [':%s=%s' % (k,name(d[k])) 
            for k in sorted(d.keys() ) 
            if k[0] is not "_"]
    return '{'+' '.join(show)+'}'
