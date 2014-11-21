# kagrawa1: Script to calculate stats for svn log files

import re, json, pymongo
import gzip, sys, os, shutil, pickle, collections
from operator import itemgetter, attrgetter
from collections import Counter

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

  cmtSize = {'2007':0, '2008':0, '2009':0, '2010':0, '2011':0,'2012':0, '2013':0, '2014':0 }
  uniqCmt  = {'2007':[], '2008':[], '2009':[] , '2010':[] , '2011':[] ,'2012':[] , '2013':[], '2014':[] }
  uniqCmtSize = {'2007':0, '2008':0, '2009':0, '2010':0, '2011':0,'2012':0, '2013':0, '2014':0 }
  authors  = {'2007':[], '2008':[], '2009':[] , '2010':[] , '2011':[] ,'2012':[] , '2013':[], '2014':[] }
  deltaYr  = {'2007':0, '2008':0, '2009':0, '2010':0, '2011':0,'2012':0, '2013':0, '2014':0 }
  totalCmt = {'2007':[], '2008':[], '2009':[] , '2010':[] , '2011':[] ,'2012':[] , '2013':[], '2014':[] }
  preyear = 0
  
  # It's SVN

  line = text.strip().split('__NEWLINE__\n') 		 #get all the commits

  # get the info of each commit
  for cmt in line:
    splits = cmt.split(';')
    # There may be semicolons in the comments too
    props = splits[:7]
    year = props[3][:4]                 # get year as every list will be year driven

    revision = props[0]                                  #revision number
    valrev   = totalCmt[year]

    if revision not in valrev:                           #commit each year
       totalCmt[year].append(revision)

    author  = props[1]                                   #name of author
    valauth = authors[year] 
    if author not in valauth:
       #authNum[year] += 1 
       authors[year].append(author)  

    comment        = ';'.join(splits[6:])
    cmtSize[year] += len(comment)                        #comment Size
    valcmt  = uniqCmt[year]
    if comment not in valcmt:
       uniqCmt[year].append(comment)                    
       uniqCmtSize[year] += len(comment)                 #unique cmt size
       #uniqCmtCount[year] += 1                           #unique cmt 

    deltaYr[year] += 1

  return totalCmt, uniqCmt, authors, cmtSize, uniqCmtSize, deltaYr


def decode(text):
    return str(text).encode('string_escape')

if __name__ == '__main__':

  # Get list of files
  files = open('list_svn', 'r').readlines()
  counter = 0
  for f in files:
    f = f.strip() 
    name = f 
    contents = open(f).read()

    totalCmt, uniqCmt, authors, cmtSize, uniqCmtSize, deltaYr  = parse(contents, name)

    for key in sorted(uniqCmt.keys()):
        if len(totalCmt[key]) == 0:
	   totalCmt[key].append('DivideByZeroCheck')
        if len(uniqCmt[key]) == 0:
           uniqCmt[key].append('DivideByZeroCheck')
        if len(authors[key]) == 0:
           authors[key].append('DivideByZeroCheck')

    print "\nFor file : ", name
    print "\n Year   #nTC            #nUC    	#Au	     cmtSize  	unqCmtSize 	delta         #QC         #UC/Au"  
    for key in sorted(uniqCmt.keys()):
        print key, ": ", len(totalCmt[key]), "		", len(uniqCmt[key]), "		", len(authors[key]), "		", cmtSize[key], "	", uniqCmtSize[key], "		", deltaYr[key], "		", float(len(uniqCmt[key]))/float(len(totalCmt[key])), "		", float(len(uniqCmt[key]))/float(len(authors[key]))


#    print "totalCmt: ", collections.OrderedDict(sorted(totalCmt.items()))
#    print "uniqCmtCount: ", collections.OrderedDict(sorted(uniqCmtCount.items()))
#    print "authNum: ", collections.OrderedDict(sorted(authNum.items()))
#    print "uniqCmtSize: ", collections.OrderedDict(sorted(uniqCmtSize.items()))
#    print "cmtSize: ", collections.OrderedDict(sorted(cmtSize.items()))
#    print "deltaYr: ", collections.OrderedDict(sorted(deltaYr.items()))
