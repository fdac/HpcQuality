import re, json, pymongo
import gzip, sys, os, shutil, pickle

def parse(text, name):
  size = 0
  data = {}
  data['name'] = name
  data['commits'] = []
  if text == '':
    return (0, {}, {})
  last_revision = ''
  authors = {}
  delta = 0
  files = {}
  text = text .replace('\r', '')
  # For svn
  changes = text.strip().split('__NEWLINE__\n')
  commit = {}
  size += len (text)
  ct = 0
  for change in changes:
    splits = change.split(';')
    # There may be semicolons in the comments too
    props = splits[:7]
#    print "props: ",  props 
    comment = ';'.join(splits[6:])
#    print "comment: ", comment                    # comment   - 6
    revision = props[0]
    authors [props[1]] = 1                        # author    - 1
#    print "author: ", props[1]
    files [props[4]] = 1                          # files     - 4
#    print "files: ",props[4]
    delta += 1
    ct += 1
    
#    if (ct > 10):
#       break
   
    
  return delta, authors, files

def decode(text):
    return str(text).encode('string_escape')

if __name__ == '__main__':

  # Get list of files
  files = open('klist', 'r').readlines()  
  counter = 0
  for f in files:
    f = f.strip()
#    print 'files: ', f    
    contents = open( f).read()
#    print contents
    name = f
    delta,authors,files = parse(contents, name)
    na = len(authors.keys())
    nf = len(files.keys())
    print "\n\n ********" 
    #print f + ';' + name + ';' + str(delta) + ';' + str(na)+ ';' + str(nf) + ';' + ':'.join (authors.keys()) + ';' + ':'.join(files.keys())
    print f + ';' + name + ';' + str(delta) + ';' + str(na)+ ';' + str(nf)

