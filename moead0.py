from __future__ import division,print_function
import sys,random,re
sys.dont_write_bytecode =True

def THE(f=None,cache={}):
  "To keep the options, cache their last setting."
  if not f: 
    return cache
  def wrapper(**d):
    tmp = cache[f.__name__] = f(**d)
    return tmp
  return wrapper

@THE
def TILE(**d): 
  return o(
    cf = 0.5,
    f  = 0.3,
  ).update(**d)

def THAT(this,s=""):
  d = this.dict()
  for x in sorted(d.keys()):
    prin(s + ('%s = ' % x))
    y = d[x]
    THAT(y,s+"\t") if isinstance(y,o) else print(y)
     
rand= random.random
seed= random.seed

class Cache:
  def __init__(i,max=128): i.n,i.lst = 0,[None]*max
  def tell(i,x):
    i.n, l = i.n + 1, len(i.lst)
    if rand() <= l/i.n: i.lst[ int(rand()*l) ] = x
  def kept(i): 
    return [x for x in i.lst if not x is None]
  def cliff(i,j):
    more, less, l1, l2 = 0, 0, i.kept(), j.kept()
    for x in l1:
      for y in l2:
        if x > y : more += 1
        if x < y : less += 1
    return (more - less)/(len(l1)*len(l2))

def shuffle(lst): random.shuffle(lst); return lst

def prin(*l): 
  sys.stdout.write(', '.join(map(str,l)))
 
def fun(x): 
  return x.__class__.__name__ == 'function'

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

def data(w,row):
  for col in w.num:
    val = row[col]
    w.min[col] = min(val, w.min.get(col,val))
    w.max[col] = max(val, w.max.get(col,val))

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

def indep(w,cols):
  for col in cols:
    if col in w.indep: yield col

class Col:
  def any(self): return None
  def dist(self, x, y): return 0
  def norm(self, x) : return x
  def interpolate(self, x, y, z): return None

class N(Col):
  def __init__(i,lo=0,hi=1):
    i.lo, i.hi = lo,hi
  def __iadd__(i,x):
    i.lo = min(i.lo,x)
    i.hi = max(i.hi,x)
    return i
  def dist(i,x,y): return (x - y)**2
  def any(i): return i.lo + rand()*(i.hi - i.lo)
  def interpolate(i,x,y,z,w):
    return x + w.f*(y-z) if rand() < w.cf else x
  def norm(i,x):
    tmp = (i - i.lo) / (i.hi - i.lo + 0.00001)
    return max(0,min(tmp,1))

def nearest(w,row):
  def norm(val,col):
    lo, hi = w.min[col], w.max[col]
    return (val - lo ) / (hi - lo + 0.00001)
  def dist(centroid):
    n,d = 0,0
    for col in indep(w, w.num):
      x1,x2 = row[col], centroid[col]
      n1,n2 = norm(x1,col), norm(x2,col)
      d    += (n1 - n2)**2
      n    += 1
    for col in indep(w, w.sym):
      x1,x2 = row[col],centroid[col]
      d    += (0 if x1 == x2 else 1)
      n    += 1
    return d**0.5 / n**0.5
  lo, out = 10**32, None
  for n,(_,_,_,centroid) in enumerate(w.centroids):
    d = dist(centroid)
    if d < lo:
      lo,out = d,n
  return out

if __name__ == '__main__': _genic()

