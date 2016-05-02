#!/usr/bin/python

# PBDB Taxa By Ref as Indexed Lookup Service
#
# @author: jlauters

import re
import sys
import json
import requests
from pymongo import MongoClient

search = sys.argv[1]

def taxa_by_ref(base_name):
  print "searching: " + base_name

  pbdb = requests.get("https://paleobiodb.org/data1.2/taxa/byref.json?base_name=" + base_name + "&ref_type=all")
  if 200 == pbdb.status_code:
    pbdb_json = json.loads(pbdb.content)
    records = pbdb_json['records']

    references = {}
    # merge single ref data for each result
    for record in records:

      ref_id = record['rid'].replace("ref:", "")
      
      rank = ""
      if "rnk" in record:
        rank = record['rnk']

      tdf = ""
      if "tdf" in record:
        tdf = record['tdf']

      acc = ""
      if "acc" in record:
        acc = record['acc']

      acn = ""
      if "acn" in record:
        acn = record['acn']

      acr = ""
      if "acr" in record:
        acr = record['acr']

      if ref_id not in references:
        references[ref_id] = []

      references[ref_id].append({
        "tid": record['tid'], 
        "rtp": record['rtp'], 
        "name": record['nam'], 
        "rank": rank,
        "tdf": tdf,
        "acc": acc,
        "acn": acn,
        "acr": acr
        })

  return references

taxa = taxa_by_ref(search) 

print taxa['25746']
