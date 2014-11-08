class Row:
  "Place to cache info on each row"
  def __init__(i,lst,of,w=1)  : 
    i.of,i.lst=of,lst; 
    i.w = w
    i.to = {}; i.x0 = i.y0 = None
    i._objs = i._neighbors = None
  def __iter__(i): return iter( i.lst)
  def __sub__(i,j):
    if not id(j) in i.to:
      dist = i.of.m.dist(i,j)
      i.neighbor(j,dist)
      j.neighbor(i,dist)
    dist,_ = i.to[id(j)]
    return dist
  def neighbor(i,j,dist):
    i._neighbors = None
    i.to[id(j)]  = dist,j
  def closest(i) : i.neigbors(i)[0]
  def furthest(i): i.neigbors(i)[-1]
  def neighbors(i):
    if i._neighbors is None:
      i._neighbors = sorted(i.to.values())
    return i._neighbors
  def abx(i,west,east,c):
    a = i - west
    b = i - east
    x = (a**2 + c**2 - b**2)/ 2*c
    if i.x0 is None:
      y = max(0,min(1,(a**2 - x**2)))**0.5
      i.x0, i.y0 = x,y
    return a,b,x
  def objs(i):
    i._objs = i._objs or i.of.m.objs(i)
    return i._objs
