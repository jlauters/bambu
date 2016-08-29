import json
from pymongo import MongoClient

config = json.load(open('./config.json'))

# MongoDB Setup
client = MongoClient(config['mongo_url'])
db = client.test

# TODO: Pull classification_path out of pbdb_refs
#
#       -- rename pid => ref_no
#       -- reference coll_no, occ_no
#       -- get genus_name, species_name where present

# Example taxon record
# {"ref_no": "1234", "coll_no": "1234", "occ_no": "1234", "genus": "test", "species": "test", "classification_path": []}

taxon_ref_ids = []
taxon_refs = db.pbdb_taxon_lookup.find({}, {"ref_no": 1, "_id": 0})
for tf in taxon_refs:
  taxon_ref_ids.append( tf['ref_no'] )

pbdb_refs = db.pbdb_refs.find()
for ref in pbdb_refs:

    ref_no = ref['pid']
    if ref_no not in taxon_ref_ids:

      classification_path = []
      if "classification_path" in ref:
        classificaton_path = ref['classification_path']

      occ_no_arr  = []
      coll_no_arr = []
      genus_arr   = []
      species_arr = []
      pbdb_occs = db.pbdb_occurrences.find({"reference_no": ref_no})
      for occ in pbdb_occs:

        if occ['occurrence_no'] not in occ_no_arr:
          occ_no_arr.append(occ['occurrence_no'])

        if occ['collection_no'] not in coll_no_arr:
          coll_no_arr.append(occ['collection_no'])

        if occ['genus_name'] not in genus_arr:
          genus_arr.append(occ['genus_name'])

        if occ['species_name'] not in species_arr:
          species_arr.append(occ['species_name'])


      db.pbdb_taxon_lookup.insert_one({
        "ref_no": ref_no,
        "coll_no": coll_no_arr,
        "occ_no": occ_no_arr,
        "genus": genus_arr,
        "species": species_arr,
        "classification_path": classification_path})
