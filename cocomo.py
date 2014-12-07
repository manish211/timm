from __future__ import division,print_function
import sys,random
sys.dont_write_bytecode = True

any = random.choice
rseed = random.seed

## lib

def mult(lst): return reduce(lambda x,y: x*y,lst)

def ranges(t=None):
  t = t or Coc2tunings
  out= {k:[n+1 for n,v in enumerate(lst) if v]
          for k,lst in t.items()}
  out["kloc"] = xrange(2,1001)
  return out

def f7(z)   : return '%7.1f' % z
def pretty(txt,x): 
  print(txt+',',', '.join(map(f7,xtiles(x))))

def xtiles(lst,div=10,parts=[1,3,5,7,9]):
  v   = lambda x: lst[x][0]
  lst = sorted(lst)
  q   = len(lst) // div
  return [v(0)]+[v(q*n) for n in parts]+[v(-1)]

## Cocomo
_  = None;  Coc2tunings = dict(
#              vlow  low   nom   high  vhigh  xhigh   
  Flex=[        5.07, 4.05, 3.04, 2.03, 1.01,    _],
  Pmat=[        7.80, 6.24, 4.68, 3.12, 1.56,    _],
  Prec=[        6.20, 4.96, 3.72, 2.48, 1.24,    _],
  Resl=[        7.07, 5.65, 4.24, 2.83, 1.41,    _],
  Team=[        5.48, 4.38, 3.29, 2.19, 1.01,    _],
  acap=[        1.42, 1.19, 1.00, 0.85, 0.71,    _],
  aexp=[        1.22, 1.10, 1.00, 0.88, 0.81,    _],
  cplx=[        0.73, 0.87, 1.00, 1.17, 1.34, 1.74],
  data=[           _, 0.90, 1.00, 1.14, 1.28,    _],
  docu=[        0.81, 0.91, 1.00, 1.11, 1.23,    _],
  ltex=[        1.20, 1.09, 1.00, 0.91, 0.84,    _],
  pcap=[        1.34, 1.15, 1.00, 0.88, 0.76,    _], 
  pcon=[        1.29, 1.12, 1.00, 0.90, 0.81,    _],
  pexp=[        1.19, 1.09, 1.00, 0.91, 0.85,    _], 
  pvol=[           _, 0.87, 1.00, 1.15, 1.30,    _],
  rely=[        0.82, 0.92, 1.00, 1.10, 1.26,    _],
  ruse=[           _, 0.95, 1.00, 1.07, 1.15, 1.24],
  sced=[        1.43, 1.14, 1.00, 1.00, 1.00,    _], 
  site=[        1.22, 1.09, 1.00, 0.93, 0.86, 0.80], 
  stor=[           _,    _, 1.00, 1.05, 1.17, 1.46],
  time=[           _,    _, 1.00, 1.11, 1.29, 1.63],
  tool=[        1.17, 1.09, 1.00, 0.90, 0.78,    _])
 
def COCOMO2(project, t=Coc2tunings,a=2.94, b=0.91): 
  sfs, ems, kloc = 0, 1, 10
  for k,setting in project.items():
    if k == 'kloc':
      kloc = setting
    else:
      values = t[k]
      value  = values[setting - 1]
      if k[0].isupper: sfs += value
      else           : ems *= value
  return a * ems * kloc**(b + 0.01 * sfs)

def guess(d):
  return {k:any(x) for k,x in d.items()}

def _coc(proj,seed=1,n=1000):  
  rseed(seed)
  settings, estimates = ranges(), []
  for _ in xrange(n):
    settings = guess(settings)
    guessed  = guess(proj())
    settings.update(guessed)
    estimates += [COCOMO2(settings),guessed]
  pretty(proj.__name__, estimates)
 
def ok(f):
  all    = ranges()
  prefix = f.__name__
  for k,some in f().items():
    if not k in all:
      raise KeyError( '%s.%s' % (prefix,k))
    else:
      possible   = all[k]
      impossible = list(set(some) - set(possible))
      if impossible:
        raise IndexError( '%s.%s=%s' % 
                          (prefix,k,impossible))
  return f

@ok
def demo1(): return dict()

@ok
def demo2(): return dict(kloc=xrange(2,11),docu=[2,3,4,5])

#_coc(demo1)
#_coc(demo2)
#exit()

def keys(proj,seed=1,n=1000,enough=0.75): 
  rseed(seed)
  lo, hi,log = {}, {}, []
  for _ in xrange(n):
    settings = guess(ranges())
    guessed  = guess(proj())
    settings.update(guessed)
    est  = COCOMO2(settings)
    mad  = risks(settings)
    kloc = settings["kloc"]
    log += [(est,kloc,mad,guessed)]
    for k,v in [('kloc',kloc),('est',est),('mad',mad)]:
      lo[k] = min(v, lo.get(k,   10**32))
      hi[k] = max(v, hi.get(k,-1*10**32))
  best={}; rest={}
  scores=[]
  for est0,kloc0,mad0,guessed in log:
    est1  = norm(est0,  "est",  lo, hi)
    kloc1 = norm(kloc0, "kloc", lo, hi) 
    mad1  = norm(mad0,  "mad",  lo, hi) 
    score = 1 - ((est1**2 + (1-kloc1)**2 + mad1) **0.5 / (3**0.5))
    scores += [(score,guessed)]
  scores = sorted(scores)
  rests = at = int(enough*n)
  bests = n - rests
  border  = scores[at][0]
  for score,guessed in sorted(scores):
    what = best if score > border else rest
    for k,v in guessed.items():
      what[(k,v)] = what.get((k,v),0) + 1
  br = []
  #print(best)
  for (k,v),b0 in best.items():
    r0 = rest.get((k,v),0)
    b = b0/bests
    r = r0/rests
    if b < r:
      score = b**2/(b+r)
      br += [(score,(k,v))]
  print(sorted(br))


def norm(v,x,lo,hi):
  return (v - lo[x]) / (hi[x] - lo[x] + 0.0001)

def risks(project):
  risk = 0
  for (x1,x2),m in Mad.items():
    v1    = project[x1] 
    v2    = project[x2]
    risk += m[v1 - 1][v2 - 2]
  return risk

Mad={}

Mad[('sced','cplx')] = Mad[('sced','time')] = [
 [0,0,0,1,2,4],
 [0,0,0,0,1,2],
 [0,0,0,0,0,1],
 [0,0,0,0,0,0],
 [0,0,0,0,0,0],
 [0,0,0,0,0,0]]

Mad[('sced','rely')] =  Mad[('sced','pvol')] = [
 [0,0,0,1,2,0],
 [0,0,0,0,1,0],
 [0,0,0,0,0,0],
 [0,0,0,0,0,0],
 [0,0,0,0,0,0],
 [0,0,0,0,0,0]]

Mad[('ltex','pcap')] = Mad[('sced','acap')] = \
Mad[('sced','pexp')] = Mad[('sced','pcap')] = \
Mad[('sced','aexp')] = [
 [4,2,1,0,0,0],
 [2,1,0,0,0,0],
 [1,0,0,0,0,0],
 [0,0,0,0,0,0],
 [0,0,0,0,0,0],
 [0,0,0,0,0,0]]

Mad[('sced','tool')] = Mad[('sced','ltex')] = \
Mad[('sced','Pmat')] = Mad[('Pmat','acap')] = \
Mad[('tool','acap')] = Mad[('tool','pcap')] = \
Mad[('tool','Pmat')] = Mad[('Team','aexp')] = \
Mad[('Team','sced')] = Mad[('Team','site')] = [
 [2,1,0,0,0,0],
 [1,0,0,0,0,0],
 [0,0,0,0,0,0],
 [0,0,0,0,0,0],
 [0,0,0,0,0,0],
 [0,0,0,0,0,0]]

Mad[('rely','acap')] = Mad[('rely','Pmat')] = \
Mad[('rely','pcap')] = [
 [0,0,0,0,0,0],
 [0,0,0,0,0,0],
 [1,0,0,0,0,0],
 [2,1,0,0,0,0],
 [4,2,1,0,0,0],
 [0,0,0,0,0,0]]

Mad[('cplx','acap')] = Mad[('cplx','pcap')] = \
Mad[('cplx','tool')] = Mad[('stor','acap')] = \
Mad[('time','acap')] = Mad[('ruse','aexp')] = \
Mad[('ruse','ltex')] = Mad[('Pmat','pcap')] = \
Mad[('stor','pcap')] = Mad[('time','pcap')] = [
 [0,0,0,0,0,0],
 [0,0,0,0,0,0],
 [0,0,0,0,0,0],
 [1,0,0,0,0,0],
 [2,1,0,0,0,0],
 [4,2,1,0,0,0]]

Mad[('pvol','pexp')] = [
 [0,0,0,0,0,0],
 [0,0,0,0,0,0],
 [0,0,0,0,0,0],
 [1,0,0,0,0,0],
 [2,1,0,0,0,0],
 [0,0,0,0,0,0]]

Mad[('time','tool')] = [
 [0,0,0,0,0,0],
 [0,0,0,0,0,0],
 [0,0,0,0,0,0],
 [0,0,0,0,0,0],
 [1,0,0,0,0,0],
 [2,1,0,0,0,0]]

#_coc(proj=demo2); exit()

keys(demo2);
#exit()
def COCONUT(training,          # list of projects
            a=10, b=1,         # initial  (a,b) guess
            deltaA    = 10,    # range of "a" guesses 
            deltaB    = 0.5,   # range of "b" guesses
            depth     = 10,    # max recursive calls
            constricting=0.66):# next time,guess less
  if depth > 0:
    useful,a1,b1= GUESSES(training,a,b,deltaA,deltaB)
    if useful: # only continue if something useful
      return COCONUT(training, 
                     a1, b1,  # our new next guess
                     deltaA * constricting,
                     deltaB * constricting,
                     depth - 1)
  return a,b

def GUESSES(training, a,b, deltaA, deltaB,
           repeats=20): # number of guesses
  useful, a1,b1,least,n = False, a,b, 10**32, 0
  while n < repeats:
    n += 1
    aGuess = a1 - deltaA + 2 * deltaA * rand()
    bGuess = b1 - deltaB + 2 * deltaB * rand()
    error  = ASSESS(training, aGuess, bGuess)
    if error < least: # found a new best guess
      useful,a1,b1,least = True,aGuess,bGuess,error
  return useful,a1,b1

def ASSESS(training, aGuess, bGuess):
   error = 0.0
   for project in training: # find error on training
     predicted = COCOMO2(project, aGuess, bGuess)
     actual    = effort(project)
     error    += abs(predicted - actual) / actual
   return error / len(training) # mean training error

def nasa93():
  vl=1;l=2;n=3;h=4;vh=5;xh=6
  return dict(
    sfem=21,
    kloc=22,
    effort=23,
    names= [ 
     # 0..8
     'Prec', 'Flex', 'Resl', 'Team', 'Pmat', 'rely', 'data', 'cplx', 'ruse',
     # 9 .. 17
     'docu', 'time', 'stor', 'pvol', 'acap', 'pcap', 'pcon', 'aexp', 'plex',  
     # 18 .. 25
     'ltex', 'tool', 'site', 'sced', 'kloc', 'effort', '?defects', '?months'],
    projects=[
	[h,h,h,vh,h,h,l,h,n,n,n,n,l,n,n,n,n,n,h,n,n,l,25.9,117.6,808,15.3],
	[h,h,h,vh,h,h,l,h,n,n,n,n,l,n,n,n,n,n,h,n,n,l,24.6,117.6,767,15.0],
	[h,h,h,vh,h,h,l,h,n,n,n,n,l,n,n,n,n,n,h,n,n,l,7.7,31.2,240,10.1],
	[h,h,h,vh,h,h,l,h,n,n,n,n,l,n,n,n,n,n,h,n,n,l,8.2,36,256,10.4],
	[h,h,h,vh,h,h,l,h,n,n,n,n,l,n,n,n,n,n,h,n,n,l,9.7,25.2,302,11.0],
	[h,h,h,vh,h,h,l,h,n,n,n,n,l,n,n,n,n,n,h,n,n,l,2.2,8.4,69,6.6],
	[h,h,h,vh,h,h,l,h,n,n,n,n,l,n,n,n,n,n,h,n,n,l,3.5,10.8,109,7.8],
	[h,h,h,vh,h,h,l,h,n,n,n,n,l,n,n,n,n,n,h,n,n,l,66.6,352.8,2077,21.0],
	[h,h,h,vh,h,h,l,h,n,n,xh,xh,l,h,h,n,h,n,h,h,n,n,7.5,72,226,13.6],
	[h,h,h,vh,n,n,l,h,n,n,n,n,l,h,vh,n,vh,n,h,n,n,n,20,72,566,14.4],
	[h,h,h,vh,n,n,l,h,n,n,n,n,l,h,h,n,vh,n,h,n,n,n,6,24,188,9.9],
	[h,h,h,vh,n,n,l,h,n,n,n,n,l,h,vh,n,vh,n,h,n,n,n,100,360,2832,25.2],
	[h,h,h,vh,n,n,l,h,n,n,n,n,l,h,n,n,vh,n,l,n,n,n,11.3,36,456,12.8],
	[h,h,h,vh,n,n,l,h,n,n,n,n,h,h,h,n,h,l,vl,n,n,n,100,215,5434,30.1],
	[h,h,h,vh,n,n,l,h,n,n,n,n,l,h,h,n,vh,n,h,n,n,n,20,48,626,15.1],
	[h,h,h,vh,n,n,l,h,n,n,n,n,l,h,n,n,n,n,vl,n,n,n,100,360,4342,28.0],
	[h,h,h,vh,n,n,l,h,n,n,n,xh,l,h,vh,n,vh,n,h,n,n,n,150,324,4868,32.5],
	[h,h,h,vh,n,n,l,h,n,n,n,n,l,h,h,n,h,n,h,n,n,n,31.5,60,986,17.6],
	[h,h,h,vh,n,n,l,h,n,n,n,n,l,h,h,n,vh,n,h,n,n,n,15,48,470,13.6],
	[h,h,h,vh,n,n,l,h,n,n,n,xh,l,h,n,n,h,n,h,n,n,n,32.5,60,1276,20.8],
	[h,h,h,vh,h,h,l,h,n,n,n,n,l,n,n,n,n,n,h,n,n,l,19.7,60,614,13.9],
	[h,h,h,vh,h,h,l,h,n,n,n,n,l,n,n,n,n,n,h,n,n,l,66.6,300,2077,21.0],
	[h,h,h,vh,h,h,l,h,n,n,n,n,l,n,n,n,n,n,h,n,n,l,29.5,120,920,16.0],
	[h,h,h,vh,n,h,n,n,n,n,h,n,n,n,h,n,h,n,n,n,n,n,15,90,575,15.2],
	[h,h,h,vh,n,h,n,h,n,n,n,n,n,n,h,n,h,n,n,n,n,n,38,210,1553,21.3],
	[h,h,h,vh,n,n,n,n,n,n,n,n,n,n,h,n,h,n,n,n,n,n,10,48,427,12.4],
	[h,h,h,vh,h,n,vh,h,n,n,vh,vh,l,vh,n,n,h,l,h,n,n,l,15.4,70,765,14.5],
	[h,h,h,vh,h,n,vh,h,n,n,vh,vh,l,vh,n,n,h,l,h,n,n,l,48.5,239,2409,21.4],
	[h,h,h,vh,h,n,vh,h,n,n,vh,vh,l,vh,n,n,h,l,h,n,n,l,16.3,82,810,14.8],
	[h,h,h,vh,h,n,vh,h,n,n,vh,vh,l,vh,n,n,h,l,h,n,n,l,12.8,62,636,13.6],
	[h,h,h,vh,h,n,vh,h,n,n,vh,vh,l,vh,n,n,h,l,h,n,n,l,32.6,170,1619,18.7],
	[h,h,h,vh,h,n,vh,h,n,n,vh,vh,l,vh,n,n,h,l,h,n,n,l,35.5,192,1763,19.3],
	[h,h,h,vh,h,h,l,h,n,n,n,n,l,n,n,n,n,n,h,n,n,l,5.5,18,172,9.1],
	[h,h,h,vh,h,h,l,h,n,n,n,n,l,n,n,n,n,n,h,n,n,l,10.4,50,324,11.2],
	[h,h,h,vh,h,h,l,h,n,n,n,n,l,n,n,n,n,n,h,n,n,l,14,60,437,12.4],
	[h,h,h,vh,n,h,n,h,n,n,n,n,n,n,n,n,n,n,n,n,n,n,6.5,42,290,12.0],
	[h,h,h,vh,n,n,n,h,n,n,n,n,n,n,n,n,n,n,n,n,n,n,13,60,683,14.8],
	[h,h,h,vh,h,n,n,h,n,n,n,n,n,n,h,n,n,n,h,h,n,n,90,444,3343,26.7],
	[h,h,h,vh,n,n,n,h,n,n,n,n,n,n,n,n,n,n,n,n,n,n,8,42,420,12.5],
	[h,h,h,vh,n,n,n,h,n,n,h,n,n,n,n,n,n,n,n,n,n,n,16,114,887,16.4],
	[h,h,h,vh,h,n,h,h,n,n,vh,h,l,h,h,n,n,l,h,n,n,l,177.9,1248,7998,31.5],
	[h,h,h,vh,h,h,l,h,n,n,n,n,l,n,h,n,n,n,n,n,n,n,302,2400,8543,38.4],
	[h,h,h,vh,h,n,h,l,n,n,n,n,h,h,n,n,h,n,n,h,n,n,282.1,1368,9820,37.3],
	[h,h,h,vh,h,h,h,l,n,n,n,n,n,h,n,n,h,n,n,n,n,n,284.7,973,8518,38.1],
	[h,h,h,vh,n,h,h,n,n,n,n,n,l,n,h,n,h,n,h,n,n,n,79,400,2327,26.9],
	[h,h,h,vh,l,l,n,n,n,n,n,n,l,h,vh,n,h,n,h,n,n,n,423,2400,18447,41.9],
	[h,h,h,vh,h,n,n,n,n,n,n,n,l,h,vh,n,vh,l,h,n,n,n,190,420,5092,30.3],
	[h,h,h,vh,h,n,n,h,n,n,n,h,n,h,n,n,h,n,h,n,n,n,47.5,252,2007,22.3],
	[h,h,h,vh,l,vh,n,xh,n,n,h,h,l,n,n,n,h,n,n,h,n,n,21,107,1058,21.3],
	[h,h,h,vh,l,n,h,h,n,n,vh,n,n,h,h,n,h,n,h,n,n,n,78,571.4,4815,30.5],
	[h,h,h,vh,l,n,h,h,n,n,vh,n,n,h,h,n,h,n,h,n,n,n,11.4,98.8,704,15.5],
	[h,h,h,vh,l,n,h,h,n,n,vh,n,n,h,h,n,h,n,h,n,n,n,19.3,155,1191,18.6],
	[h,h,h,vh,l,h,n,vh,n,n,h,h,l,h,n,n,n,h,h,n,n,n,101,750,4840,32.4],
	[h,h,h,vh,l,h,n,h,n,n,h,h,l,n,n,n,h,n,n,n,n,n,219,2120,11761,42.8],
	[h,h,h,vh,l,h,n,h,n,n,h,h,l,n,n,n,h,n,n,n,n,n,50,370,2685,25.4],
	[h,h,h,vh,h,vh,h,h,n,n,vh,vh,n,vh,vh,n,vh,n,h,h,n,l,227,1181,6293,33.8],
	[h,h,h,vh,h,n,h,vh,n,n,n,n,l,h,vh,n,n,l,n,n,n,l,70,278,2950,20.2],
	[h,h,h,vh,h,h,l,h,n,n,n,n,l,n,n,n,n,n,h,n,n,l,0.9,8.4,28,4.9],
	[h,h,h,vh,l,vh,l,xh,n,n,xh,vh,l,h,h,n,vh,vl,h,n,n,n,980,4560,50961,96.4],
	[h,h,h,vh,n,n,l,h,n,n,n,n,l,vh,vh,n,n,h,h,n,n,n,350,720,8547,35.7],
	[h,h,h,vh,h,h,n,xh,n,n,h,h,l,h,n,n,n,h,h,h,n,n,70,458,2404,27.5],
	[h,h,h,vh,h,h,n,xh,n,n,h,h,l,h,n,n,n,h,h,h,n,n,271,2460,9308,43.4],
	[h,h,h,vh,n,n,n,n,n,n,n,n,l,h,h,n,h,n,h,n,n,n,90,162,2743,25.0],
	[h,h,h,vh,n,n,n,n,n,n,n,n,l,h,h,n,h,n,h,n,n,n,40,150,1219,18.9],
	[h,h,h,vh,n,h,n,h,n,n,h,n,l,h,h,n,h,n,h,n,n,n,137,636,4210,32.2],
	[h,h,h,vh,n,h,n,h,n,n,h,n,h,h,h,n,h,n,h,n,n,n,150,882,5848,36.2],
	[h,h,h,vh,n,vh,n,h,n,n,h,n,l,h,h,n,h,n,h,n,n,n,339,444,8477,45.9],
	[h,h,h,vh,n,l,h,l,n,n,n,n,h,h,h,n,h,n,h,n,n,n,240,192,10313,37.1],
	[h,h,h,vh,l,h,n,h,n,n,n,vh,l,h,h,n,h,h,h,n,n,l,144,576,6129,28.8],
	[h,h,h,vh,l,n,l,n,n,n,n,vh,l,h,h,n,h,h,h,n,n,l,151,432,6136,26.2],
	[h,h,h,vh,l,n,l,h,n,n,n,vh,l,h,h,n,h,h,h,n,n,l,34,72,1555,16.2],
	[h,h,h,vh,l,n,n,h,n,n,n,vh,l,h,h,n,h,h,h,n,n,l,98,300,4907,24.4],
	[h,h,h,vh,l,n,n,h,n,n,n,vh,l,h,h,n,h,h,h,n,n,l,85,300,4256,23.2],
	[h,h,h,vh,l,n,l,n,n,n,n,vh,l,h,h,n,h,h,h,n,n,l,20,240,813,12.8],
	[h,h,h,vh,l,n,l,n,n,n,n,vh,l,h,h,n,h,h,h,n,n,l,111,600,4511,23.5],
	[h,h,h,vh,l,h,vh,h,n,n,n,vh,l,h,h,n,h,h,h,n,n,l,162,756,7553,32.4],
	[h,h,h,vh,l,h,h,vh,n,n,n,vh,l,h,h,n,h,h,h,n,n,l,352,1200,17597,42.9],
	[h,h,h,vh,l,h,n,vh,n,n,n,vh,l,h,h,n,h,h,h,n,n,l,165,97,7867,31.5],
	[h,h,h,vh,h,h,n,vh,n,n,h,h,l,h,n,n,n,h,h,n,n,n,60,409,2004,24.9],
	[h,h,h,vh,h,h,n,vh,n,n,h,h,l,h,n,n,n,h,h,n,n,n,100,703,3340,29.6],
	[h,h,h,vh,n,h,vh,vh,n,n,xh,xh,h,n,n,n,n,l,l,n,n,n,32,1350,2984,33.6],
	[h,h,h,vh,h,h,h,h,n,n,vh,xh,h,h,h,n,h,h,h,n,n,n,53,480,2227,28.8],
	[h,h,h,vh,h,h,l,vh,n,n,vh,xh,l,vh,vh,n,vh,vl,vl,h,n,n,41,599,1594,23.0],
	[h,h,h,vh,h,h,l,vh,n,n,vh,xh,l,vh,vh,n,vh,vl,vl,h,n,n,24,430,933,19.2],
	[h,h,h,vh,h,vh,h,vh,n,n,xh,xh,n,h,h,n,h,h,h,n,n,n,165,4178.2,6266,47.3],
	[h,h,h,vh,h,vh,h,vh,n,n,xh,xh,n,h,h,n,h,h,h,n,n,n,65,1772.5,2468,34.5],
	[h,h,h,vh,h,vh,h,vh,n,n,xh,xh,n,h,h,n,h,h,h,n,n,n,70,1645.9,2658,35.4],
	[h,h,h,vh,h,vh,h,xh,n,n,xh,xh,n,h,h,n,h,h,h,n,n,n,50,1924.5,2102,34.2],
	[h,h,h,vh,l,vh,l,vh,n,n,vh,xh,l,h,n,n,l,vl,l,h,n,n,7.25,648,406,15.6],
	[h,h,h,vh,h,vh,h,vh,n,n,xh,xh,n,h,h,n,h,h,h,n,n,n,233,8211,8848,53.1],
	[h,h,h,vh,n,h,n,vh,n,n,vh,vh,h,n,n,n,n,l,l,n,n,n,16.3,480,1253,21.5],
	[h,h,h,vh,n,h,n,vh,n,n,vh,vh,h,n,n,n,n,l,l,n,n,n,  6.2, 12,477,15.4],
	[h,h,h,vh,n,h,n,vh,n,n,vh,vh,h,n,n,n,n,l,l,n,n,n,  3.0, 38,231,12.0],
	])

