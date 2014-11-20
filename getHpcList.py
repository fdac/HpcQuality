import pymongo,re



client = pymongo.MongoClient (host="da0.eecs.utk.edu")
db = client ['bitbucket']
coll = db ['repos']

files = open('hpc_pckgList', 'r').readlines()
keywords = []

for k in files:
   text = k.lower()
   keywords.append(text.rstrip())

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


# Description of repo matching keywords
# print repo_dict


print "\n ************************************** \n" 

# Repo name matching keywords
print repo_name_dict

for x in repo_name_dict:
   print x, ":", repo_name_dict[x]



  
