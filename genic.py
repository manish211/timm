from __future__ import division,print_function
import sys,random,re
sys.dont_write_bytecode =True

def genic0(**d): return o(
    k=20,
    era=100,
    num='$',
    klass='=',
    seed=1).update(**d)

rand= random.random
seed= random.seed

def say(c):
  sys.stdout.write(c); sys.stdout.flush()

def rows(file):
  """Leaps over any columns marked 'skip'.
  Turn strings to numbers or strings. 
  Kill comments. Join lines that end in 'sep'."""
  skip, sep  = '?', ','
  bad = r'(["\' \t\r\n]|#.*)'
  def atom(x):
    try : return int(x)
    except ValueError:
       try : return float(x)
       except ValueError : return x
  def worker(): 
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
  for n,line in worker():
    todo = todo or [col for col,name in enumerate(line) 
                    if not skip in name]
    yield n, [ line[col] for col in todo ]

class o:
  """Standard trick for defining a bag of names slots
  that have no methods."""
  def __init__(i,**d): i.update(**d)
  def update(i,**d): i.__dict__.update(**d); return i
  def __repr__(i)   : 
    d    = i.__dict__
    show = [':%s %s' % (k,d[k]) 
            for k in sorted(d.keys() ) 
            if k[0] is not "_"]
    return '{'+' '.join(show)+'}'

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

def data(w,row):
  for col in w.num:
    val = row[col]
    w.min[col] = min(val, w.min.get(col,val))
    w.max[col] = max(val, w.max.get(col,val))
    
def nearest(w,row):
  def norm(val,col):
    lo, hi = w.min[col], w.max[col]
    return (val - lo ) / (hi - lo + 0.00001)
  def dist(a,b,w):
    n,d = 0,0
    for col in w.num:
      x1,x2 = a[col], b[col]
      n1,n2 = norm(x1,col), norm(x2,col)
      d    += (n1 - n2)**2
      n    += 1
    for col in w.sym:
      x1,x2 = a[col],b[col]
      d    += (0 if x1 == x2 else 1)
      n    += 1
    return d**0.5 / n**0.5
  lo, out = 10**32, None
  for n,(_,centroid) in enumerate(w.centroids):
    d = dist(row,centroid,w)
    if d < lo:
      lo,out = d,n
  return out

def move(w,row1,n):
  u0,row0 = w.centroids[n]
  u1 = 1
  out = [None]*len(row1)
  for col in w.sym:
    x0,x1 = row0[col], row1[col]
    out[col] = x1 if rand() < 1/(u0+u1) else x0
  for col in w.num:
    x0,x1= row0[col], row1[col]
    out[col] = (u0*x0 + u1*x1)/ (u0+u1)
  w.centroids[n] = (u0 + u1, out)

def less(w) :
  b4 = len(w.centroids)
  all = normu(w)
  w.centroids = [(1,row) for u,row in all if u >= rand()]
  now=len(w.centroids)
  print(" - ",b4 - now)

def normu(w):
  all  = sorted([(u,row) for u,row in w.centroids])
  most = all[-1][0]
  return [(u/most,row) for u,row in all]

def genic(datafile='data/diabetes.csv',opt=None):
  w = o(num=[], sym=[], dep=[], indep=[],
        centroids=[],
        min={}, max={}, name={},index={},
        opt=None or genic0())
  for n,row in rows(datafile):
    if n == 0: 
      header(w,row)
    else:
      data(w,row)
      if len(w.centroids) < w.opt.k:
        say("+")
        w.centroids += [(1,row)]
      else:
        move(w,row,nearest(w,row))
      if 0 == (n % w.opt.era):
        less(w)
  return sorted(normu(w),reverse=True)

def g3(row):
  for col,val in enumerate(row):
    if isinstance(val,float): 
      val = round(n,3)
    row[col] = val
  return row

for n,row in genic():
  print(n,":",g3(row))
        
      
