from __future__ import division,print_function
import sys,random,re
sys.dont_write_bytecode =True

def cached(f=None,cache={}):
  "To keep the options, cache their last setting."
  if not f: 
    return cache
  def wrapper(**d):
    tmp = cache[f.__name__] = f(**d)
    return tmp
  return wrapper

@cached
def where0(**d): 
  return o(
    div=10,
    keep=20,
    buffer= 10000,
    num='$',
    klass='=',
    seed=1).update(**d)

@cached
def rows0(**d): return o(
  skip="?",
  sep  = ',',
  num = '$',
  bad = r'(["\' \t\r\n]|#.*)'
  ).update(**d)

r= random.random
seed= random.seed
any =random.choice
def shuffle(lst): random.shuffle(lst); return lst


def say(*lst): 
  sys.stdout.write(', '.join(map(str,lst)))
 
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
    i.__dict__.update(**d); return i
  def __repr__(i)   : 
    def name(x): return x.__name__ if fun(x) else x
    d    = i.__dict__
    show = [':%s=%s' % (k,name(d[k])) 
            for k in sorted(d.keys() ) 
            if k[0] is not "_"]
    return '{'+' '.join(show)+'}'

class Sym:
  def __init__(i,init=[]):
    i.n,i.counts=0,{}
    map(i.__iadd__,init)
  def __iadd__(i,x):
    i.n += 1
    i.counts[x] = i.counts.get(x,0)+1
    return i
  def __isub__(i,x):
    i.n = max(0,i.n-1)
    if x in i.counts:
      i.counts[x] = max(0,i.counts[x]-1)
    return i

class Cache:
  def __init__(i,max=32): 
    i.n,i.max,i.items= 0,max,[]
  def __iadd__(i,x):
    i.n += 1
    m = len(i.items)
    if m< i.max     : i.items += [x]
    elif r()< m/i.n : i.items[int(r()*m)]=x
    return i

def data(m,w,row):
  for col in w.num:
    now = row[col]
    lo  = w.min[col] if col in w.min else    10**32
    hi  = w.max[col] if col in w.max else -1*10**32
    if now < lo: w.min[col] = now
    if now > hi: w.max[col] = now
        
def table(file,w):
  def chunks():
    chunk = []
    for m,row in rows(file):
      if m==0:
        header(w,row)
      else:
        data(m,w,row)
        chunk += [row]
        if len(chunk) > w.opt.buffer: 
          yield chunk
          chunk=[]
    if chunk: yield chunk
  c=-1
  for chunk in chunks():
    c += 1
    yield c,shuffle(chunk)

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

def rows(file,w=None):
  w = w or rows0()
  def prep(z):
    return float if w.num in z else str
  def lines(): 
    n,kept = 0,""
    for line in open(file):
      now   = re.sub(w.bad,"",line)
      kept += now
      if kept:
        if not now[-1] == w.sep:
          yield n, kept.split(w.sep)
          n += 1
          kept = "" 
  todo = None
  for n,line in lines():
    todo = todo or [(col,prep(name)) for col,name 
                    in enumerate(line) 
                    if not w.skip in name]
    if n: yield n, [ ready(line[col])  
                     for col,ready in todo]
    else: yield n,line

def furthest(w,row1,rows):
  most,out=-1,row1
  for row2 in rows:
    if not id(row1) == id(row2):
      d = dist(w,row1,row2)
      if d > most: 
        most,out = d,row2
  return most,out

def dist(w,row1,row2):
  def norm(val,col):
    lo, hi = w.min[col], w.max[col]
    n= (val - lo ) / (hi - lo + 0.00001)
    return n
  n,d = 0,0
  for col in indep(w, w.num):
    x1,x2 = row1[col], row2[col]
    n1,n2 = norm(x1,col), norm(x2,col)
    inc = (n1 - n2)**2
    d  += inc
    n  += 1
  for col in indep(w, w.sym):
    print("sym",sym)
    x1,x2 = row1[col],row2[col]
    inc   = (0 if x1 == x2 else 1)
    d    += inc
    n    += 1
  return d**0.5 / n**0.5

def where(src='data/diabetes.csv',opt=None):
  w = o(num=[], sym=[], dep=[], indep=[],
        tiles={},
        min={}, max={}, name={},index={},
        opt=opt or where0())
  def at(z,c): 
    return  min(opt.div-1, int(w.opt.div*z/c)) 
  first = None 
  for era,rows in table(src,w):
    print(era)
    if era == 0:
      first  = first or any(rows)
      _,west = furthest(w,first,rows)
      c,east = furthest(w,west, rows)
    for row in rows:
      a,b,c,east,west,x,y = here(w,c,row,west,east)
      k = at(x,c), at(y,c)
      if not k in w.tiles:
        w.tiles[k] = Cache(w.opt.keep)
      w.tiles[k] += row
  cluster(w.tiles,w.opt.div)
  for k,v in w.tiles.items(): 
    print(k, Sym(map(last,v.items)).counts)

def last(lst): return lst[-1]

def cluster(m,max):
  cluster1(m, 0, max-1, 0, max-1)

def cluster1(m,x0,x2,y0,y2,lvl=0,above=10**32):
  n=0
  for x,y in m.keys():
    if x0 <=  x <x2:
      if y0 <= y < y2:
        n += len(m[(x,y)].items)
  #if lvl ==3:
   # print("TILE>",x0,x2,y0,y2,[x for x in items(tile)]); exit()
  if  n < above and lvl < 10 and n > 10:
    say('|..' * lvl)
    print('[%s:%s][%s:%s] #%s.' % (x0,x2,y0,y2,n))
    x1 = int(x0 + (x2-x0)/2)
    y1 = int(y0 + (y2-y0)/2)
    for xa,xb,ya,yb in [(x0,x1,y0,y1),
                        (x0,x1,y1,y2),
                        (x1,x2,y0,y1),
                        (x1,x2,y1,y2)]:
      cluster1(m,xa,xb,ya,y2,lvl+1,n)

def items(lst):
  if isinstance(lst,(list,tuple)):
    for x in lst:
      for y in items(x):
        yield y
  else:
    yield lst
              
def here(w,c,row,west,east):
  delta = 1 + 1/w.opt.div
  while True:
    a,b = dist(w,row,west), dist(w,row,east)
    if   a > (c*delta): west = row
    elif b > (c*delta): east = row
    else: 
      x = (a*a + c*c - b*b)/(2*c+0.00001)
      y = max(0,a*a - x*x)**0.5
      return a,b,c,east,west,x,y
    c = dist(w,west,east); say("+")

def _where( src='data/diabetes.csv'):
  if len(sys.argv) == 2:
    src= sys.argv[1]
  opt=where0()
  seed(opt.seed)
  where(src,opt)

if __name__ == '__main__': _where()

"""
data/diabetes2.csv (1.5M records).
caught in last gen =77%

gen | caughtLast | caughtAll | dob     | $preg | $plas  | $pres | $skin | $insu  | $mass | $pedi | $age  | =class        
1   | 205        | 390       | 1571001 | 2.04  | 97.08  | 65.03 | 23.25 | 52.6   | 29.19 | 0.35  | 24.14 | testednegative
2   | 146        | 2408      | 1560001 | 3.77  | 117.73 | 74.08 | 0.79  | 3.86   | 31.04 | 0.4   | 31.84 | testedpositive
3   | 119        | 824       | 1566001 | 7.54  | 142.17 | 78.47 | 7.53  | 16.58  | 29.72 | 0.46  | 52.1  | testednegative
4   | 109        | 252       | 1571002 | 2.39  | 145.63 | 73.09 | 30.13 | 201.47 | 34.58 | 0.35  | 28.57 | testednegative
5   | 106        | 2690      | 1554001 | 8.03  | 106.6  | 76.56 | 32.07 | 64.18  | 34.63 | 0.41  | 40.84 | testednegative
6   | 85         | 654       | 1569002 | 1.62  | 118.5  | 70.76 | 33.44 | 119.23 | 36.16 | 0.93  | 26.23 | testedpositive
genic0 {:buffer=500 :era=1000 :k=8 :klass== :num=$ :seed=1 :tiny=halfEraDivK}
rows0 {:bad=(["\' \t\r\n]|#.*) :sep=, :skip=?}

real	3m25.949s
user	3m7.403s
sys	0m2.315s
"""
