from __future__ import division,print_function
import sys,random,re
sys.dont_write_bytecode =True

class o:
  def __init__(i,**d): i.update(**d)
  def update(i,**d): 
    i.dict().update(**d); return i
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
  def wrapper(**d):
    tmp = cache[f.__name__] = f(**d)
    return tmp
  print(f.__name__,cache)
  return wrapper

@THE
def MOEAD0(**d): return o(
    cf = 0.5,
    f  = 0.3,
  ).update(**d)

@THE
def LIB(**d): return o(
    buffer = 128
  ).update(**d)

def say(*l):
  sys.stdout.write(', '.join(map(str,l))) 

def THAT(this,s=""):
  print(2)
  d = this.dict()
  print(3,d)
  for x in sorted(d.keys()):
    print(x)
    say(s + ('%s = ' % x))
    y = d[x]
    THAT(y,s+"\t") if isinstance(y,o) else print(y)

print(1)
THAT(THE())
exit()
     
r   = random.random
seed= random.seed
ask = random.choice

def cliffsDelta(lst1, lst2):
  more = less = 0
  for x in lst1:
    for y in lst2:
      if x > y : more += 1
      if x < y : less += 1
  d = (more - less) / (len(lst1)*len(lst2))
  # Thresholds are from http://goo.gl/25bAh9
  if   abs(d) < 0.147 : return 0 # negligible
  elif abs(d) < 0.33  : return 0 # small
  elif abs(d) < 0.474 : return 2 # medium
  else:                 return 3 # large

def shuffle(lst): random.shuffle(lst); return lst
def fun(x): return x.__class__.__name__=='function'

def g(lst,n=3):
  for col,val in enumerate(lst):
    if isinstance(val,float): val = round(val,n)
    lst[col] = val
  return lst

def printm(matrix):
  s = [[str(e) for e in row] for row in matrix]
  lens = [max(map(len, col)) for col in zip(*s)]
  fmt = ' | '.join('{{:{}}}'.format(x) for x in lens)
  for row in [fmt.format(*row) for row in s]:
    print(row)


def data(w,row):
  for col in w.num: col.tell(row[col])

def header(w,row):
  def numOrSym(val):
    return w.num if w.opt.num in val else w.sym
  def indepOrDep(val):
    return w.dep if w.opt.klass in val else w.indep
  for col,val in enumerate(row):
    numOrSym(val).append(col)
    indepOrDep(val).append(col)
    w.name[col] = val
    w.index[val] = col

class N:
  def __init__(i,lo=0,hi=0):
    i.n,i.lo,i.hi = 0,lo,hi,
    i.size  = THE().LIB.size
    i._kept = [None]*i.size
  def tell(i,x):
    i.n += 1
    i.lo, i.hi = min(i.lo,x), max(i.hi,x)
    l = len(i._kepy)
    if r() <= l/i.n: i._kept[ int(r()*l) ]= x
  def kept(i): 
    return [x for x in i.lst if x is not None]
  def dist(i,x,y): 
    x1, y1 = i.norm(x), i.norm(y)
    return (x1 - y1)
  def ask(i): 
    return i.lo + r()*(i.hi - i.lo)
  def interpolate(i,x,y,z,w):
    return x + w.f*(y-z) if r() < w.cf else x
  def norm(i,x):
    tmp = (i - i.lo) / (i.hi - i.lo + 0.00001)
    return max(0,min(tmp,1))
  def smear(i,x,y,z,w):
    return x + w.f*(y-z) if r() < w.cf else x

c=N([x for x in xrange(10000)])
print(sorted(c._cache))


class W: # words
  def __init__(i,txt,all=None): i.all = all or {}
  def tell(i,x)  : i.all[x] = True
  def ask(i)     : return(ask(i.all.keys()))
  def dist(i,x,y): return 0 if x==y else 1
  def norm(i,x)  : return x
  def smear(i,x,y,z,w):
    if r() >= w.cf:  return x
    w = y if r() <= w.f else z 
    return x if r() <= 0.5 else w

class Row:
  def __init__(i,lst,of=None): 
    i.of = of; i.to={}
    i.x0,i.y0,i.to,i.lst = None,None,None,lst
  def iter(i): return iter(i.lst)
  def __getattr__(i,x): return i.lst[x]
  def __setattr__(i,x,y): i.lst[x] = y
  def abx(i,west,east,c):
    a = i - west
    b = i - east
    x = (a**2 + c**2 - b**2)/ (2**c)
    if i.x0 is None:
      i.x0 = x
      i.y0 = max(0,min(1,(a**2 - x**2)))**0.5
    return a,b,x
  def dist(i,j):
    d = sum(c.dist(i[c.pos],j[c.pos]) 
            for c in i.of.ins)
    return d**0.5 / len(i.of.ins)**0.5
  def __sub__(i,j):
    if id(j) in i.to:
      return i.to[id(j)][0]
    d = i.dist(i,j)
    i.to[id(j)] = (d,j)
    j.to[id(i)] = (d,i)
    return d

if __name__ == '__main__': _genic()

