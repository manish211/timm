def  facet(f):
  n = f.__name__
  def wrapper(i,*lst): 
    old = i.facets
    k = (n,tuple(map(id,lst))) if lst else n 
    x = old[k] = old[k] if k in old else f(i,*lst)
    return x
  return wrapper


class Fred:
  def __init__(i): 
    i.facets={}
  @facet
  def n(i,j=100):
    print("J:",j)
    return j+len(i.__class__.__name__)

f = Fred()
print(f.n())
print(f.n(20))
print(f.n(21))
print(f.facets)
