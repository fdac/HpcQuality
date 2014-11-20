import re, json, pymongo
import gzip, sys, os, shutil, pickle

def parse(text, name):
  size = 0
  data = {}
  data['name'] = decode(name)
  data['commits'] = []
  if text == '':
    return (0, {}, {})
  last_revision = ''
  authors = {}
  delta = 0
  files = {}
  text = text .replace('\r', '')
  revs = {}
  totalCmt = {'2007':0, '2008':0,'2009':0, '2010':0, '2011':0,'2012':0, '2013':0, '2014': 0  }
  authNum  = {'2007':0, '2008':0,'2009':0, '2010':0, '2011':0,'2012':0, '2013':0, '2014': 0  }
  uniqCmt  = {'2007':0, '2008':0,'2009':0, '2010':0, '2011':0,'2012':0, '2013':0, '2014': 0  }
  comments = {'2007':0, '2008':0,'2009':0, '2010':0, '2011':0,'2012':0, '2013':0, '2014': 0  }
  commSize = {'2007':0, '2008':0,'2009':0, '2010':0, '2011':0,'2012':0, '2013':0, '2014': 0  }
  preyear = 0

  # Determine if it uses Git
  if text.find('ENDOFCOMMENT') > 0 and text[:text.find(';')].find(':') > 0:
    # It's Mercurial
    cmts = text.strip().split('ENDOFCOMMENT\n') #get all the commits
    #commit = {}
    #size += len (text)
    # get the info of each commit
    for cmt in cmts:
      splits = cmt.split(';')
      # There may be semicolons in the comments too
      props = splits[:7]
      comment = ';'.join(splits[7:])

      revision = props[0]   #number of revision = total number of commits
      author = decode(props[5]) #name of author
    #  authors [decode(props[5])] = 1 # list of unique authors

      #files [decode(props[3])] = 1   # list of unique files been changed
      #delta += 1 #total number of files been changed (include duplicated files)
      
      #get the year of the commit
      year = props[4][:4]

      #number of total commits each year
      if revision not in revs:
         revs[revision] = 1
         totalCmt[year] += 1

      #number of unique commits each year   
      if comment not in comments:
         comments[comment] = 1
         try:
            uniqCmt[year] = uniqCmt[year] + 1
            commSize[year] += len(comment) #total size of unique comments
         except:
            pass

      elif int(year) != preyear:
          try:
             uniqCmt[year] += 1
             commSize[year] += len(comment) #total size of unique comments
          except:
             pass

      #number of authors contributed each year
      if author not in authors:
        authors[author] = 1
        authNum[year] += 1
      elif year != preyear:
        authors[author] = 1
        authNum[year] += 1
 
      preyear = year

  ####### TO DO ...
  else:
    # It's Git
    size += len (text)
    lines = text.splitlines()
    commit = {}
    for line in lines:
      props = line.split(';')
      revision = props[0]
      authors [decode(props[3])] = 1  #a list of unique authors
      if len (props) > 8:
        files [decode(props[8])] = 1  #a list of unique files changed
      else: sys.stderr.write ('Bad format:' + ';'.join(props) + '\n')
      delta += 1                      #total number of times for files changed
 # return delta, authors, files
  return totalCmt, uniqCmt, commSize, authors

def chunks(l, n):
    if n < 1: 
        n = 1
    return [l[i:i + n] for i in range(0, len(l), n)]

def decode(text):
    return str(text).encode('string_escape')

if __name__ == '__main__':
  delta_dir = './LogFiles_HPC/'
  #delta_dir = '/home/audris/hpc/'
  #client = pymongo.MongoClient(host="da0.eecs.utk.edu")
  #db = client['bitbucket']
  #deltas = db['measures']

  # Get list of files
  files = open('mlist', 'r').readlines()
  counter = 0
  for f in files:
    f = f.strip() #strip the blank space from the beginning or end of the string
    name = f .replace ('log', '') .replace ('.bb.txt', '') #remove the redundant text from the file name
    #name = f .replace ('bitbucket.org_', '') .replace ('.delta.gz', '')
#    print 'files: ', f, "name: ", name, 'open : ', delta_dir + f
    #contents = gzip.open(delta_dir + f).read()
    contents = open(delta_dir + f).read() #file has been decompressed
    #delta,authors,files = parse(contents, name)

    totalCmt, uniqCmt, commSize, authors = parse(contents, name)

    #get the info of commits quality each year
    for a in totalCmt.keys():
      #Quality of commits
      #unique commits/total commits
      
      cmtQli = uniqCmt[a] / totalCmt[a]
      sizeCmt = commSize[a] / uniqCmt[a] 
      cmtPerAu = uniqCmt[a] / authCmt[a]     
 
      print name + ';' + str(a) + ';' + str(totalCmt[a]) + ';' + str(uniqCmt[a]) + ';' +  str(cmtQli)+ ';' + str(sizeCmt)+ ';' + str(cmtPerAu)

 #   na = len(authors.keys())
 #   nf = len(files.keys())
 #   print f + ';' + name + ';' + str(delta) + ';' + str(na)+ ';' + str(nf) + ';' + ':'.join (authors.keys()) + ';' + ':'.join(files.keys())
	    
