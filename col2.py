from __future__ import division,print_function
import sys, random
sys.dont_write_bytecode =True

from lib2 import *

class Col:
  def __init__(i,tag='',col=None):
    i.tag,i.col,i.n = tag,col,1
    i.setup()
  def __iadd__(i,x):
    if x != "?": 
      i.n += 1
      i.add(x)
    return i

class S(Col):
  def setup(i): i.cnt,i.most,i.mode = {},0,None
  def xpect(i): return i.mode
  def norm(i,x): return x
  def str2col(x): return x
  def add(i,x): 
    tmp  = i.cnt[x] = i.cnt.get(x,0) + 1
    if tmp > i.most:
      i.most, i.mode = tmp,x

class N(Col):
  def xpect(i): return i.mu
  def str2col(x): return float(x)
  def setup(i): 
    i.mu = i.m2 = 0
    i.lo,i.hi = 10**32,-1*10**32
  def add(i,x):
    i.lo, i.hi = min(i.lo,x), max(i.hi,x)
    delta = x - i.mu
    i.mu += delta/i.n
    i.m2 += delta*(x - i.mu)
  def sd(i): 
    if i.n < 2: return 0
    else:       
      return (max(0,i.m2)/(i.n - 1))**0.5
  def norm(i,x):
    all = x.hi - x.lo + 0.00001
    return max(0,min(1, (x - x.lo)/all))
