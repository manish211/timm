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
    keys = [k for k in sorted(i.d().keys()) 
            if k[0] is not "_"]
    print(keys)
    show = [':%s=%s' % (k, name(i.d()[k])) 
            for k in keys]
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

def THAT(x=the,s="",pre=""):
  d = x.d()
  say(pre)
  for k in sorted(d.keys()):
    if k[0] is not "_":
      say(s + (':%s ' % k))
      y = d[k]
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

class N:
  def __init__(i,init=[],lo=None,hi=None,name=''):
    i.n, i.lo, i.hi, i.name = 0,lo,hi,name
    i._kept = [None]*the.LIB.buffer
    map(i.tell,init)
  def ask(i)     : return i.lo + r()*(i.hi - i.lo)
  def dist(i,x,y): return i.norm(x) - i.norm(y)
  def log(i): return N(name=i.name,lo=i.lo,hi=i.hi)
  def tell(i,x):
    i.n += 1
    if i.lo is None: i.lo = x
    if i.hi is None: i.hi = x
    i.lo, i.hi = min(i.lo,x), max(i.hi,x)
    l = len(i._kept)
    if r() <= l/i.n: i._kept[ int(r()*l) ]= x
    return x
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
  def __repr__(i): 
    return '{:%s * %s [%s .. %s]}'%(
      i.name,i.n,i.lo ,i.hi)

class W: # words
  def __init__(i,all=None,name=''): 
    i.all = all or {}
    i.name=name
  def tell(i,x)  : 
    i.all[x] = i.all.get(x,0) + 1
    return x
  def ask(i)     : return(ask(i.all.keys()))
  def dist(i,x,y): return 0 if x==y else 1
  def norm(i,x)  : return x
  def log(i)  : return W(name=i.name)
  def smear(i,x,y,z):
    m = the.MOEAD0
    if r() >= m.cf:  return x
    w =    y if r() <= m.f else z 
    return x if r() <= 0.5 else w

def  facet(f):
  n = f.__name__
  def wrapper(i,*lst): 
    old = i.facets
    k = (n,tuple(map(id,lst))) if lst else n 
    x = old[k] = old[k] if k in old else f(i,*lst)
    return x
  return wrapper

class Row:
  def __init__(i,of,lst=None): 
    i.facets={}
    i.of, i.lst = of, lst or []
  def iter(i) : return iter(i.lst)
  def __getattr__(i,x) : return i.lst[x]
  def abx(i,west,east,c):
    a = i.dist(west)
    b = i.dist(east)
    x = (a**2 + c**2 - b**2)/ (2**c)
    i.x0y0(a,x)
    return a,b,x
  @facet
  def x0y0(i,a,x):
    return x, max(0,min(1,(a**2 - x**2)))**0.5
  @facet
  def objs(i,keep=True):
    those = [obj(i) for obj in i.of.m.objs()]
    if keep:
      for one, tell in zip(those,i.of.tells.objs): # XXX position
        tell.tell(one)
    return those 
  def dist(i,j,other=True):
    return j.dist(i,False) if other else i.d(i,j)
  @facet
  def d(i,j):
      total = sum(c.dist(i[c.pos],j[c.pos]) 
                  for c in i.of.ins)
      return total**0.5 / len(i.of.ins)**0.5
  def smear(i,j,k): # somethimes want a zombie row XXX
    return Row(of,[in1.smear(x,y,z) 
                   for x,y,z, in1 in
                   zip(i,j,k, i.of.ins)])

class Feeling:
  def __init__(i,f,love=True) : 
    i.f, i.name, i.love = f, f.__name__, love
  def __call__(i,*l) : return i.f(*l)
  def __repr__(i)    : return '%s(%s)' % (
      ('Love' if i.love else 'Hate'),
      i.name)
  def howBad(i,x): 
    return 1 - x if i.love else x

def love(f): return Feeling(f,love=True)
def hate(f): return Feeling(f,love=False)

def model(**d):
  return o(ins=[],outs=[],objs=[]).update(**d)

def Schaffer():
  @hate
  def f1(x): return x[0]**2
  @hate
  def f2(x): return (x[0]-2)**2
  return model(
    ins  = [N(name="x1",lo=-4,hi=4)],
    objs = [f1,f2])
  
class Table:
  def __init__(i,model):
    i.rows, i.factory, i.m = [], model, model()
    i.objs = [N(name=f.name) for f in i.m.objs]
    i.asks =o(ins = i.m.ins,
              outs= i.m.outs + i.m.objs)
    i.tells=o(
      ins=  [x.log() for x in i.m.ins ],
      outs= [x.log() for x in i.m.outs] + i.objs)
  def ask(i):
    row = Row(i, [remember.tell(generate.ask())
                  for generate, remember in
                  zip(i.asks.ins, i.tells.ins)])
    i.rows += [row]
    return row
  def smear(i):
    one,two,three = any(rows),any(rows),any(rows)
    return one.smear(two,three)
    

    
    
