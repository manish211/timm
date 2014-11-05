from __future__ import division,print_function
import sys
sys.dont_write_bytecode =True

from table2 import *

@THE
def GENIC(**d): 
  def halfEraDivK(w): 
    return w.the.era/w.the.k/2.5
  return o(
    k     = 20,
    era   = 100,
    buffer= 512,
    tiny  = halfEraDivK,
    num   = '$',
    klass = '=').update(**d)

def fuse(w,new,n):
  u0,u,dob,old = w.centroids[n]
  u1 = 1
  out = [None]*len(old)
  for col in w.sym:
    x0,x1 = old[col], new[col]
    out[col] = x1 if rand() < 1/(u0+u1) else x0
  for col in w.num:
    x0,x1= old[col], new[col]
    out[col] = (u0*x0 + u1*x1)/ (u0+u1)
  w.centroids[n] = (u0 + u1,u+u1, dob, out)

def more(w,n,row):
  w.centroids += [(1,1,n,row)]

def less(w,n) :
  b4 = len(w.centroids)
  w.centroids = [(1,u,dob,row) 
                 for u0,u,dob,row in w.centroids 
                 if u0 > w.the.tiny(w)]
  print("at n=%s, pruning %s%% of clusters" % (
         n,  int(100*(b4 - len(w.centroids))/b4)))

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

def report(w,clusters):
  cols = w.index.keys()
  header = sorted(w.name.keys())
  header= [w.name[i] for i in header]
  matrix = [['gen','caughtLast',
              'caughtAll','dob'] + header]
  caught=0
  for m,(u0,u,dob,centroid) in enumerate(clusters):
    if u0 > w.the.tiny(w):
      caught += u0
      matrix += [[m+1,u0,u,dob] + g(centroid,2)]
  print("\ncaught in last gen =%s%%\n" %
        int(100*caught/w.the.era))
  printm(matrix)

def genic(src='data/diabetes.csv',the=None,zip=None):
  w = o(num=[], sym=[], dep=[], indep=[],
        centroids=[],
        min={}, max={}, name={},index={},
        the=the or GENIC())
  for n, row in table(src,w,zip=zip):
    data(w,row)
    if len(w.centroids) < w.the.k:
      more(w,n,row)
    else:
      fuse(w,row,nearest(w,row))
      if not (n % w.the.era):
        less(w,n)
  return w,sorted(w.centroids,reverse=True)

def _genic(src='diabetes.csv'):
  if len(sys.argv) == 2:
    src= sys.argv[1]
  print(src)
  the=GENIC(k=8,era=67)
  seed(the.seed)
  report(*genic(src,the=the,
                zip='data/data.zip')) 

if __name__ == '__main__': _genic()

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
