import time
from datetime import datetime
from dateutil.parser import parse
n2u = {}
e2u = {}
rstats = {}
ustats = {}
stats = {}
cmt = {}
if __name__ == '__main__':
  f = open ('listU.out')
  for l in f:
    ar = l .rstrip () .split(';')
    u, n = ar[0], ar[1]
    n2u [n] = u
  f = open ('email2name.out')
  for l in f:
    ar = l .rstrip () .split(';')
    n = ar [0]
    email = ar [1]
    u = ar [2]
    if u in n2u: u = n2u [u]
    e2u [email] = u
  f = open ('RepoSize.csv')
  for l in f: 
    ar = l .rstrip () .split(';')
    vcs = ar [1]
    fr = str(time.mktime(parse(ar[3]).timetuple()))
    to = str(time.mktime(parse(ar[4]).timetuple()))
    s = ar [0]
    n = ar [5]
    u = n .split ("/")[0]
    n = n .replace ("/","_")
    rstats [n] = (vcs, s, fr, to, u)
  us = open('cntFlws.out', 'r').readlines()
  for u in us:
    u = u.strip()
    n, nFl, nFd, flws, fwd = u.split(';')
    ustats [n] = (nFl, nFd)
  repos = open('cntWch.out', 'r').readlines()
  for repo in repos:
    repo = repo.strip()
    n, nW, nFr, nPu, w, f, p = repo.split(';')
    n = n .replace('/', '_')
    stats [n] = (nW, nFr, nPu)
  repos = open('Project2/repoCommentQualityNew.r', 'r').readlines()
  for repo in repos:
    repo = repo.strip()
    ar = repo.split(';')
    ar .pop (0)
    n = ar .pop (0)
    cmt [n] = ar
  print "repo;nW;nFr;nPu;nDe;nAuEmail;nAu;nFi;vcs;Siz;from;to;u;nFl;nFd;Authors;nUniqCmt;nCmt;cmtTotLen;pct0;pct10;pct20;pct30;pct40;pct50;pct60;pct70;pct80;pct90;pct95;pct99;pct100";
  repos = open('measures.out', 'r').readlines()
  for repo in repos:
    repo = repo.strip()
    n, nDe, nAu, nFi, authors, files = repo.split(';')
    nW, nFr, nPu = ("0", "0", "0")
    if n not in rstats:
      continue
    if n in stats:
       nW, nFr, nPu = stats [n]
    aus = authors .split(':')
    aus1 = set()
    for a in aus:
      tmp = a
      if a in e2u: tmp = e2u [a]
      aus1 .add (tmp)
    aus2 = ':'.join(list(aus1))
    nAu2 = str(len (aus2))
    vcs, Siz, fr, to, u = rstats [n]
    nFl, nFd = ("0", "0")
    if u in ustats:
      nFl, nFd = ustats [u]
    res = list ([n, nW, nFr, nPu, nDe, nAu, nAu2, nFi, vcs, Siz, fr, to, u, nFl, nFd, aus2 ])
    if n in cmt:
      res.extend (cmt[n])
    else:
      res.extend ([""] * 16)
    print ';' .join (res)
