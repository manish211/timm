from __future__ import division,print_function
import sys,random,re
sys.dont_write_bytecode =True

def settings(**d): return o(
  name="KEYSWEST v0.1",
  what="A linear-time MOEA/D variant",
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
  author="Tim Menzies",
  copyleft="(c) 2014, MIT license, http://goo.gl/3UYBp",
  secure = False,
  seed=1,
  tiny=0.5,
  start='print(The._logo)',
  cache = o(size=256),
  read  = o(sep      = ",",
            bad      = r'(["\' \t\r\n]|#.*)',
            skip     = '?',
            numc     = '$',
            less     = '<',
            more     = '>',
            klass    = '=',
            missing  = '?',
            )
  ).update(**d)

class o:
  def __init__(i,**d): i.update(**d)
  def update(i,**d): i.__dict__.update(**d); return i
  def __repr__(i)   : 
    d    = i.__dict__
    show = [':%s %s' % (k,d[k]) 
            for k in sorted(d.keys() ) 
            if k[0] is not "_"]
    return '{'+' '.join(show)+'}'

The= settings()

rand= random.random
seed= random.seed
any = random.choice
def gt(x,y): return x > y
def lt(x,y): return x < y

def say(*lst):
  sys.stdout.write(' '.join(map(str,lst)))
  sys.stdout.flush()
def sayln(*lst):
  say(*lst); print("")

def _say(): sayln(1,2,3,4)

def cmd(com=The.start):
  if not The.secure:
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
  tbl = o(rows=[],head=None)
  for n,cells in row(source): 
    if n == 0 : 
      f = factory0(cells)
      tbl.head = f()
      meta = tbl.head.cols[0]
    else : 
      cells = [meta] + cells
      tbl.head += cells
      tbl.rows += [cells]
  return tbl

def row(file):
  """Leaps over any columns marked 'skip'.
  Turn strings to numbers or strings. 
  Kill comments. Join lines that end in 'sep'."""
  skip = The.read.skip
  sep  = The.read.sep
  bad  = The.read.bad
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
  def __iadd__(i,x):
    if not x is None:
      i.add(x)
    return i

class Cache(Col):
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
  def add(i,x):
    i.n += 1
    if len(i.all) < The.cache.size: # if not full
      i._has = None
      i.all += [x]               # then add
    else: # otherwise, maybe replace an old item
      if rand() <= The.cache.size/i.n:
        i._has=None
        i.all[int(rand()*The.cache.size)] = x
  def has(i):
    if i._has == None:
      i.all  = sorted(i.all)
      med,iqr = medianIQR(i.all,ordered=True)
      i._has = o(
        median = med,      iqr = iqr,
        lo     = i.all[0], hi  = i.all[-1])
    return i._has

class N(Col):
  "For nums"
  def __init__(i,col=0,least=None,most=None,name=None):
    i.col=col
    i.name=None
    i.least, i.most=least,most  
    i.lo,i.hi = 10**32, -1*10**32
    i.cache   = Cache()
  def add(i,x):
    if not (None == i.least == i.most):
      assert x >= i.least and x <= i.most
    i.cache += x
  def norm(i,x):
    z = i.cache.has()
    tmp = (x - z.lo)/ (z.hi - z.lo + 0.00001)
    tmp =  max(0,min(1,tmp))
    print("T",x,tmp)
    return tmp
  def dist(i,x,y):
    return i.norm(x) - i.norm(y)
    
class S(Col):
  "For syms"
  def __init__(i,col=0,items=[],name=None):
    i.index = frozenset(items)
    i.items = items
    i.col=col
    i.name=name 
    i.counts={}
    i.mode, i.most = None,0
  def any(i):
    return random.choice(i.items)
  def __iadd__(i,x):
    if i.index:
      assert x in i.index
    n = i.counts[x] = i.counts.get(x,0) + 1
    if n > i.most:
      i.mode, i.most = x,n
  def dist(i,x,y): return 0 if x == y else 1

class O(Col):
  "for objectives"
  def __init__(i,col=0,f=lambda x: 1,name=None,
    love=False # for objectives to maximize, set love to True
    ):
    i.f=f
    i.col=col
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
  def add(i,x):
    i.n += x
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
    return i
  def __repr__(i):
    return i.of.name + '*' + str(i.weight)

def head(lst):
  def sym(x)  : return not The.read.numc  in x
  def num(x)  : return The.read.numc in x
  def less(x) : return The.read.less in x and num(x)  
  def more(x) : return The.read.more in x and num(x)
  def klass(x): return The.read.klass in x and sym(x)
  def w(n,x):
    y = N if num(x) else S
    y = y()
    y.name, y.col = x, n
    y.klass, y.less, y.more = klass(x), less(x), more(x)
    return y
  return [w(n,x) for n,x in enumerate(lst)]

class Cols:
  def __init__(i,factory,cols=[],name=None):
    i.cols = [Meta(i)] + cols
    i.factory, i.name  = factory, factory.__name__
    i.nums = [];  i.syms = []; i.objs = []; 
    i.indep= []; i.dep = [];  i.less = []; i.more = []
    for pos,header in enumerate(i.cols):
      header.col = pos 
      if pos >= 1:
        if isinstance(header,N): i.nums += [header]
        if isinstance(header,S): i.syms += [header]
        if header.less or header.more or \
           isinstance(header,O): i.objs += [header]
        if header.klass:         i.dep  += [header]
    i.indep = i.nums + i.syms
  def any(i): return [z.any() for z in i.cols]
  def __iadd__(i,lst):
    i.add(lst)
    return i
  def add(i,lst): 
    for z in i.indep: z += lst[z.col]
    for z in i.dep:   z += lst[z.col]
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
  def dist(i,lst1,lst2):
    total,c = 0,len(i.indep)
    print(3333)
    for x,y,indep in vals(lst1,lst2,i.indep):
      inc =  indep.dist(x,y)**2
      print("I>",x,y,inc)
      total += inc
    d= total**0.5/c**0.5        
    return d


def factory0(lst):
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

def closest(row1, rows, best=10**32):
  id1, cols, out  = id(row1), row1[0], row1
  print(best)
  for row2 in rows:
    id2 = id(row2)
    if id2 > id1:
      print(id1,id2)
      tmp = cols.dist(row1,row2)
      print("D>",tmp,id1,id2)
      print("  ",row1)
      print("  ",row2)
      if tmp < best:
        print(tmp)
        best,out = tmp,row2
        exit()
        return best
  return out

def furthest(row, rows):
  return closest(row, rows,best=-1,better=gt)

tbl = table('data/nasa93.csv')

# for col in tbl.head.nums:
#   print(col.name,col.cache.has())

# for col in tbl.head.syms:
#   print(col.name,col.counts)

# for n1,row1 in enumerate(tbl.rows):
#   for n2,row2 in enumerate(tbl.rows):
#     if n1 > n2:
#       print(n1,n2,tbl.head.dist(row1,row2))

print("\n=========================================")

for row1 in tbl.rows:
  row2 = closest(row1,tbl.rows)
  #row3 = furthest(row1,tbl.rows)
  #print("\n",row1,"\n",row2," <== closest\n",row3," <== furthest")
      
