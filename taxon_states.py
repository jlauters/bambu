import json
from pymongo import MongoClient

config = json.load(open('./config.json'))

# MongoDB Setup
client = MongoClient(config['mongo_url'])
db = client.test

# TODO: Pull states out of pbdb_refs
#

pbdb_refs = db.pbdb_refs.find()
for ref in pbdb_refs:

  states = []
  
  # if states in ref
  if "states" in ref and ref['states'] is not None:
    states = ref['states']

  # else check collection
  else:
    collection = db.pbdb_colls.find({"reference_no": ref['pid']})
    for col in collection:
      states.append(coll['state'])

  print "for ref: " + ref['pid'] + " we found ..."
  print states

  db.pbdb_taxon_lookup.update({"ref_no": ref['pid']},{"$set": { "states": states }})
