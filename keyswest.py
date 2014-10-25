from __future__ import division,print_function
import sys,random,re
sys.dont_write_bytecode =True

def settings(**d): return o(
  name="KEYSWEST v0.1",
  what="A linear-time MOEA/D variant",
  synopsis="""
  Read tabular data from disk.  Find 'islands'-
  leaves of a dendogram found via recursive PCA-like
  clustering. Then discretize the numerics via
  minimizing the entropy of the island ids
  associated with the numeric values.  Apply 'envy'
  to find islands 'better' than some 'current'
  island.  Sort ranges via their frequency in better
  and current.  Greedy search the sort to find the
  best fewest ranges.
  """,
  _logo="""
            .-""-.
           / .--. \ 
          / /    \ \ 
          | |    | |
          | |.-""-.|
         ///`.::::.`\ 
        ||| ::/  \:: ;
        ||; ::\__/:: ;
         \\\ '::::' /
     jgs  `=':-..-'`
    """,
  author="Tim Menzies",
  copyleft="(c) 2014, MIT license, http://goo.gl/3UYBp",
  seed=1,
  tiny=0.5,
  start='print(The._logo)',
  cache = o(size=256),
  reader= o(sep      = ",",
            bad      = r'(["\' \t\r\n]|#.*)',
            skip     ='?',
            numc     ='$',
            missing  = '?',
            )
  ).update(**d)

class o:
  def __init__(i,**d): i.update(**d)
  def update(i,**d): i.__dict__.update(**d); return i

The= settings()

rand= random.random
seed= random.seed
any = random.choice

def say(*lst):
  sys.stdout.write(' '.join(map(str,lst)))
  sys.stdout.flush()
def sayln(*lst):
  say(*lst); print("")

def _say(): sayln(1,2,3,4)

def cmd(com=The.start):
  if globals()["__name__"] == "__main__":
    if len(sys.argv) == 3:
      if sys.argv[1] == '--cmd':
        com = sys.argv[2] + '()'
    if len(sys.argv) == 4:
        com = sys.argv[2] + '(' + sys.argv[3] + ')'
    eval(com)

def medianIQR(lst, ordered=False):
  lst = lst if ordered else sorted(lst)
  n   = len(lst)
  q   = n//4
  iqr = lst[q*3] - lst[q]
  if n % 2:  return lst[q*2],iqr
  p = max(0,q-1)
  return (lst[p] + lst[q]) * 0.5,iqr

def atom(x):
  try : return int(x)
  except ValueError:
    try : return float(x)
    except ValueError : return x

#########################################################

def table(source):
  tbl = o(rows=[],cols=None)
  for n,cells in row(source): 
    if n == 0 : 
      f = factory(cells)
      tbl.cols = f(); exit()
    else : 
      tbl.cols += cells
  return tbl

def row(file):
  """Leaps over any columns marked 'skip'.
  Turn strings to numbers or strings. 
  Kill comments. Join lines that end in 'sep'."""
  skip = The.reader.skip
  sep  = The.reader.sep
  bad  = The.reader.bad
  def rows(): 
    n,kept = 0,""
    for line in open(file):
      now   = re.sub(bad,"",line)
      kept += now
      if kept:
        if not now[-1] == sep:
          yield n, map(atom, kept.split(sep))
          n += 1
          kept = "" 
  todo = None
  for n,line in rows():
    todo = todo or [col for col,name in enumerate(line) 
                    if not skip in name]
    yield n, [ line[col] for col in todo ]

def _rows(f='data/nasa93.csv'):
   for n,cells in row(f): 
     print(n,cells)



#########################################################
class Col:
  def any(i): return None
  def dist(i,x,y): return 0
  def norm(i,x) : return x

class Cache:
  "Keep a random sample of stuff seen so far."
  def any(i): return any(i.all)
  def dist(i,x,y): 
    return i.norm(x) - i.norm(y)
  def norm(i,x):
    has = i.has()
    return (x- has().lo) / (has.hi- has.lo + 0.00001)
  def __init__(i,inits=[]):
    i.all,i.n,i._has = [],0,None
    map(i.__iadd__,inits)
  def __iadd__(i,x):
    i.n += 1
    if len(i.all) < The.cache.size: # if not full
      i._has = None
      i.all += [x]               # then add
    else: # otherwise, maybe replace an old item
      if rand() <= The.cache.size/i.n:
        i._has=None
        i.all[int(rand()*The.cache.size)] = x
    return i
  def has(i):
    if i._has == None:
      lst  = sorted(i.all)
      med,iqr = medianIQR(i.all,ordered=True)
      i._has = o(
        median = med,      iqr = iqr,
        lo     = i.all[0], hi  = i.all[-1])
    return i._has

class N(Col):
  "For nums"
  def __init__(i,col=0,least=0,most=1,name=None):
    i.col=col
    i.name=None
    i.least, i.most=least,most  
    i.lo,i.hi = 10**32, -1*10**32
  def __iadd__(i,x):
    assert x >= i.least and x <= i.most
    i.lo = min(i.lo,x)
    i.hi = max(i.hi,x)
    return i
  def norm(i,x):
    tmp = (x - i.lo)/ (i.hi - i.lo + 0.00001)
    return max(0,min(1,tmp))
  def dist(i,x,y):
    return i.norm(x) - i.norm(y)
    
class S(Col):
  "For syms"
  def __init__(i,col=0,items=[],name=None):
    i.index = frozenset(items)
    i.items = items
    i.col=col
    i.name=name 
  def any(i):
    return random.choice(i.items)
  def __iadd__(i,x): 
    assert x in i.index
  def dist(i,x,y): return 0 if x == y else 0

class O(Col):
  "for objectives"
  def __init__(i,col=0,f=lambda x: 1,name=None,
    love=False # for objectives to maximize, set love to True
    ):
    i.f=f
    i.love=love
    i.name= name or f.__name__
    i.n= N(col=col,least= -10**32, most=10**32)
  def score(i,lst):
    x = lst[i.col]
    if x == None:
        x = i.f(lst)
        i.n += x
        lst[i.col] = x
    return x
  def height(i):
    return i.n.norm(i._score)
  def better(i,x,y):
    return x > y if i.love else x < y
  def worse(i,x,y):
    return x < y if i.love else x > y
  
class Meta(Col):
  id=0
  def __init__(i,of,weight=1):
    i.weight, i.of, i.klass = weight, of, None
    i.id = Meta.id = Meta.id + 1
  def any(i):
    return Meta(i.of)
  def __repr__(i):
    return i.of.name + ':' \
           + ('DEAD' if i.dead else 'ALIVE') \
           + '*' + str(i.weight)

def head(lst):
  def w(n,x):
    y = N if The.reader.numc in x else S
    y = y()
    y.name, y.col = n, x
  return [w(n,x) for n,x in enumerate(lst)]


class Cols:
  def __init__(i,factory,cols=[]):
    i.cols = [Meta(i)] + cols
    i.factory, i.name  = factory, factory.__name__
    i.nums = [];  i.syms = []; i.objs = []
    for pos,header in enumerate(i.cols):
      header.col = pos 
      if isinstance(header,N): i.nums += [header]
      if isinstance(header,S): i.syms += [header]
      if isinstance(header,O): i.objs += [header]
    i.indep = i.nums + i.syms
    i.cl    = Close()
  def any(i): return [z.any() for z in i.cols]
  def tell(i,lst): 
    for z in i.indep: z += lst[z.col]
  def score(i,l): return [z.score(l) for z in i.objs]
  def fromHell(i):
    x,c = 0, len(i.objs)
    for col in i.objs:
      tmp = col.height()
      tmp = tmp if col.love else 1 - tmp
      x += tmp**2
    return x**0.5/c**0.5
  def dominates(i,lst1,lst2):
    i.score(lst1)
    i.score(lst2)
    better=False
    for x,y,obj in vals(lst1,lst2,i.objs):
      if obj.worse(x,y) : return False
      if obj.better(x,y): better = True
    return better
  def dist(i,lst1,lst2,peeking=False):
    total,c = 0,len(i.indep)
    for x,y,indep in vals(lst1,lst2,i.indep):
      total += indep.dist(x,y)**2 
    d= total**0.5/c**0.5
    if not peeking: cl += d          
    return d

def factory(lst):
  def f():
    return Cols(f,cols=head(lst))
  return f

def vals(lst1,lst2,cols):
  for c in cols:
    yield lst1[c.col],lst2[c.col],c

def vals3(lst1,lst2,lst3,cols):
  for c in cols:
    yield lst1[c.col],lst2[c.col],lst3[c.col],c

def fromLine(a,b,c):
    x = (a**2 + c**2 - b**2)/ (2*c)
    return max(0,(a**2 - x**2))**0.5

tbl = table('data/nasa93.csv')

print(tbl.cols.cols)

 
#cmd('_close()')

