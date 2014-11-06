from __future__ import division,print_function
import sys,random,re
sys.dont_write_bytecode =True

def THE(f=None,cache={}):
  "To keep the options, cache their last setting."
  if not f: return cache
  def wrapper(**d):
    tmp = cache[f.__name__] = f(**d)
    return tmp
  return wrapper

@THE
def TILE(**d): 
  return o(
    cf = 0.5
    f  = 0.3
  ).update(**d)

def THAT(this,s=""):
  d = this.dict()
  for x in sorted(d.keys()):
    prin(s + ('%s = ' % x))
    y = d[x]
    THAT(y,s+"\t") if isinstance(y,o) else print(y)
     
rand= random.random
seed= random.seed
any = random.choice

def shuffle(lst): random.shuffle(lst); return lst

def say(*l):sys.stdout.write(', '.join(map(str,l))) 
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

class N(Col): # nums
  def __init__(i,txt,lo=0,hi=1): 
    i.txt, i.lo,i.hi = txt, 0,1
  def tell(i,x) : i.lo,i.hi= min(i.lo,x),max(i.hi,x)
  def ask(i)    : return i.lo + rand()*(i.hi-i.lo)
  def dist(i,x,y): 
    n1 = i.norm(x)
    n2 = i.norm(y)
    return n1 - n2
  def norm(i,x):
    tmp = (i - i.lo) / (i.hi - i.lo + 0.00001)
    return max(0,min(tmp,1))
  def smear(i,x,y,z):
    f, cf = THE().tile.f, THE().tile.cf
    return x + f*(y-z) if rand() < cf else x
  
def W(Col): # words
  def __init__(i,txt,all=None): i.all = all or {}
  def tell(i,x)  : i.all[x] = True
  def ask(i)     : return(any(i.cnt.keys()))
  def dist(i,x,y): return 0 if x==y else 1
  def norm(i,x)  : return x
  def smear(i,x,y,z):
    f, cf = THE().tile.f, THE().tile.cf
    if rand() >= cf:  return x
    w = y if rand() <= f else z 
    return x if rand() <= 0.5 else w

def Row:
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

