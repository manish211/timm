from __future__ import division,print_function
import re, sys, random, fnmatch, zipfile
sys.dont_write_bytecode =True

from lib2 import *
from col2 import *

@the
def rows0(**d): return o(
  skip = "?",
  sep  = ',',
  bad  = r'(["\' \t\r\n]|#.*)',
  ).update(**d)

def table(file,w,zip=None):
  def chunks():
    chunk = []
    for m,row in rows(file,zip=zip):
      if m==0:
        header(w,row)
      else:
        chunk += [row]
        if len(chunk) > w.the.buffer: 
          yield chunk
          chunk = []
    if chunk: yield chunk
  n=0
  for chunk in chunks():
    for row in shuffle(chunk):
      n += 1
      data(w,row)
      yield n,row

def header(w,row):
  def numOrSym(val):
    return w.num if w.the.num in val else w.sym
  def indepOrDep(val):
    return w.dep if w.the.klass in val else w.indep
  for col,val in enumerate(row):
    numOrSym(val).append(col)
    indepOrDep(val).append(col)
    w.name[col] = val
    w.index[val] = col

def indep(w,cols):
  for col in cols:
    if col in w.indep: yield col

def rows(src, zip=None):
  w = rows0()
  def atom(x):
    try : return int(x)
    except ValueError:
       try : return float(x)
       except ValueError : return x
  def lines(): 
    n,kept = 0,""
    for _,line in content(pattern=src,zip=zip):
      now   = re.sub(w.bad,"",line)
      kept += now
      if kept:
        if not now[-1] == w.sep:
          yield n, map(atom, kept.split(w.sep))
          n += 1
          kept = "" 
  todo = None
  for n,line in lines():
    todo = todo or [col for col,name 
                    in enumerate(line) 
                    if not w.skip in name]
    yield n, [ line[col] for col in todo ]

def content(pattern='*',zip=None):
  if zip:
    print("z")
    with zipfile.ZipFile(zip,'r') as ark:
      for file in ark.namelist():
        if fnmatch.fnmatch(file, pattern):
          with ark.open(file,'r') as lines:
            for line in lines:
              yield file,line
  else:
    for line in open(pattern,'r'):
      yield pattern,line

def data(w,row):
  for col in w.num:
    val = row[col]
    w.min[col] = min(val, w.min.get(col,val))
    w.max[col] = max(val, w.max.get(col,val))
