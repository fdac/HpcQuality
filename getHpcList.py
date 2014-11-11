import pymongo,re



client = pymongo.MongoClient (host="da0.eecs.utk.edu")
db = client ['bitbucket']
coll = db ['repos']

keywords =  ['HPC', 'climate simulation', 'molecular dynamics', 'parallel programming','FLOP', 'library tracking', 'programming model', 'fault tolerance', 'resilience', 'distributed computing', 'large scale', 'GPU', 'algorithm', 'MPI', 'SHMEM', 'openMP', 'CUDA', 'multi cores', 'scaling', 'high performance', 'latency', 'matrix', 'cluster', 'supercomputers', 'runtime',  'cloud computing', 'cluster computing', 'linear algebra', 'big data', 'large data', 'openMP', 'combustion simulation']

i=0
desc_dict = {}
repo_dict = {}
repo_name_dict = {}

for r in coll.find({}, {"description":1, "full_name":1 }):
   r_desc, r_name = (r["description"], r["full_name"])
   contained = [words for words in keywords if words in r_desc]
   if not contained:
      continue
   else: 
      for words in contained:
#         desc_dict[words] = r_desc
         repo_dict[words] = r_name

   contained_2 = [words for words in keywords if words in r_name]
   if not contained_2:
      continue
   else:
      for words in contained_2:
         repo_name_dict[words] = r_name



print repo_dict



print "\n ************************************** " 

print repo_name_dict





'''

for words in keywords:
   print coll.find({description: words})
   break

fws = {'a'}
for r in coll .find ({}, { "url":1, "values" : 1, "_id":0 } ):  
  l, v = (r ["url"], r ["values"])
  l = re.sub ("https://bitbucket.org/api/2.0/users/", "", l)
  l = re.sub ("/followers", "", l)
  fws .add (l)
  for n in v:
    f = n ["username"]
    fws .add (f)

for f in fws:
  print f .encode("utf-8")







'''

 
