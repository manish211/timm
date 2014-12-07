import random

class Retry(RuntimeError):
   def __init__(i, arg): i.args = arg


def shuffle(lst):
  random.shuffle(lst)
  return lst

def issamp(goal,w=None,retries=5):
  w = w or {}
  for _ in range(retries):
    try: 
      lurch(goal,w)
    except Retry,txt:
      retries -= 1
      if retries < 0: 
        return None
  return w

def listp(x): return isinstace(x,(list,tuple))

### undo w on failire

def lurch(lst,w={},retries=1):
  def assume(key,val):
    if key in w: 
      return val == w[key]
    w[key] = val
    return True
  def rand(ys):
    for _ in range(retries):
      good=True
      for y in shuffle(ys):
        good = good and lurch(y,w)
        if  good:
          return True
    return False
  def ror(ys):
    for _ in range(retries):
      for y in shuffle(ys):
        if lurch(y,w):
          return True
    return False  
  if listp(lst):
    op, args = lst[0], lst[1:]
    if op == 'rand': ok= rand(args)
    if op == 'ror' : ok= ror(args)
    if op == 'is'  : ok= assume(args[0],args[1])
    if op == 'not' : 
      w1 = w.copy()
      ok= not screamer(args,w1)
  else:
    ok= lst(w)
  if not ok:
    raise Retry("bad")
  else:
    return True


