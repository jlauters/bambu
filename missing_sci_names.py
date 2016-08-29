import json
import requests
import unidecode
from pymongo import MongoClient

config = json.load(open('./config.json'))
client = MongoClient(config['mongo_url'])
db = client.test

data_sources = '1|3|8|9|11|12|105|170|172'

missing = db.pbdb_refs.find({ "$and": [ {"sci_names": { "$exists": True, "$eq": []}}, { "classification_path": { "$exists": False }} ] })

print "Searching through " + str(missing.count()) + " results "

for miss in missing:

  print "checking GNP for title - " + miss['title']

  title_tokens = miss['title'].replace('<i>', '').replace('</i>', '').replace('(', '').replace(')', '').replace(',', '').replace(':', '').split()
  for token in title_tokens:
    gnparser = requests.get('http://resolver.globalnames.org/name_resolvers.json?names=' + token + '&data_source_ids=' + data_sources + '&with_vernaculars&with_context=true')

    if 200 == gnparser.status_code:
      gnp_json = json.loads( gnparser.content )

      if 'data' in gnp_json:
        known_name = gnp_json['data'][0]['is_known_name']
        if known_name and 'results' in gnp_json['data'][0]:

          print " ++++ Found Classification Path for [" + miss['pid'] + "] - " + miss['title']
          classification_path = unidecode.unidecode( gnp_json['data'][0]['results'][0]['classification_path'] )
          print "Classification Path: " + classification_path

          # If results are found but classification path is empty. Just enter the name string
          if "" == classification_path:
            classification_path = gnp_json['data'][0]['results'][0]['name_string']

          db.pbdb_refs.update({"pid": miss['pid']}, { "$addToSet": { "classification_path": classification_path }})
