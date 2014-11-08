from __future__ import division,print_function
import sys,random,re
sys.dont_write_bytecode =True

"""
"I would not give a fig for the simplicity this side
 of complexity, but I would give my life for the
 simplicity on the other side of complexity."
 -- Oliver Wendell Holmes Jr.
"""

def name(x):
  f = lambda x: x.__class__.__name__ == 'function'
  return x.__name__ if f(x) else x

class o:
  def d(i)           : return i.__dict__
  def update(i,**d)  : i.d().update(**d); return i
  def __init__(i,**d): i.update(**d)
  def __repr__(i)    :  
    show = [':%s=%s' % (k, name(i.d()[k])) 
            for k in sorted(i.d().keys() ) 
            if k[0] is not "_"]
    return '{'+' '.join(show)+'}'

the=o()
def setting(f):
  def wrapper(**d):
    tmp = the.d()[f.__name__] = f(**d)
    return tmp
  wrapper()
  return wrapper
#---------#---------#---------#---------#---------
@setting
def MOEAD0(**d): return o(
    cf = 0.5,
    f  = 0.3,
    _logo="""
    __4___
 _  \ \ \ \       "Try a little sailing
<'\ /_/_/_/        before you go buy 
 ((____!___/)           a hovercraft."
  \\0\\0\\0\\0\\/ 
 ~~~~~~~~~~~~~~~~~
  """
  ).update(**d)

@setting
def LIB(**d): return o(
    buffer = 128
  ).update(**d)

#---------#---------#---------#---------#---------
def say(*l):sys.stdout.write(', '.join(map(str,l))) 
def ako(x,y): return isinstance(x,y)

def THAT(x=tje,s="",pre=""):
  d = x.d()
  say(pre)
  for x in sorted(d.keys()):
    say(s + (':%s ' % x))
    y = d[x]
    THAT(y,s+"   ","\n") if ako(y,o) else print(y)

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
  def __init__(i,init=[],lo=None,hi=None,name=''):
    i.n,i.lo,i.hi.i.name = 0,lo,hi,name
    i._kept = [None]*the.LIB.buffer
    map(i.tell,init)
  def ask(i)     : return i.lo + r()*(i.hi - i.lo)
  def dist(i,x,y): return i.norm(x) - i.norm(y)
  def log(i)  : return N(name=i.name)
  def tell(i,x):
    i.n += 1
    if i.lo is None: i.lo = x
    if i.hi is None: i.hi = x
    i.lo, i.hi = min(i.lo,x), max(i.hi,x)
    l = len(i._kept)
    if r() <= l/i.n: i._kept[ int(r()*l) ]= x
  def kept(i): 
    return [x for x in i._kept if x is not None]
  def interpolate(i,x,y,z,w):
    return x + w.f*(y-z) if r() < w.cf else x
  def norm(i,x):
    tmp =(x - i.lo) / (i.hi - i.lo + 0.00001)
    return max(0,min(tmp,1))
  def smear(i,x,y,z):
    m = the.MOEAD0
    return x + m.f*(y-z) if r() < m.cf else x

class W: # words
  def __init__(i,all=None,name=''): 
    i.all = all or {}
    i.name=name
  def tell(i,x)  : i.all[x] = i.all.get(x,0) + 1
  def ask(i)     : return(ask(i.all.keys()))
  def dist(i,x,y): return 0 if x==y else 1
  def norm(i,x)  : return x
  def log(i)  : return W(name=i.name)
  def smear(i,x,y,z):
    m = the.MOEAD0
    if r() >= m.cf:  return x
    w =    y if r() <= m.f else z 
    return x if r() <= 0.5 else w

class Row:
  def __init__(i,of,lst=None): 
    i.to={}
    i.of.i._objs=of,None
    i.x0,i.y0,i.to,i.lst = None,None,None,lst or []
  def iter(i) : return iter(i.lst)
  def __getattr__(i,x) : return i.lst[x]
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
  def objs(i):
    i._objs= i._objs or [out1(i) 
                         for out1 in i.of.outs]
    return i._objs
  def __sub__(i,j):
    if id(j) in i.to:
      return i.to[id(j)][0]
    d = i.dist(i,j)
    i.to[id(j)] = (d,j)
    j.to[id(i)] = (d,i)
    return d

class Schaffer:
  def ins(i) : return [N(name="x1",lo=-4,hi=4)],
  def outs(i): return [i.f1,i.f2]
  def f1(i,x): return x[0]**2
  def f2(i,x): return (x[0]-2)**2

class Table:
  def __init__(i,m):
    i.m = m
    i.tell(m)              
    i.rows = []
  def tell(i,m):
    def out1(i,f): return N(name=name(f))
    i.b4  = o(ins = m.ins()
              outs= m.outs())
    i.log = o(ins = [x.log()   for x in m.ins],
              outs= [out1(f) for f in m.outs])
  def ask(i):
    def ask1(b4,log):
      val = b4.ask()
      log.tell(val)
      return val
    row = Row(i, [ask1(b4,log) for b4,log 
                  in zip(i.before.ins,i.log.ins)])
    rows += [row]
    return row
