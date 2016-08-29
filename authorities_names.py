import json
import requests
import unidecode
from pymongo import MongoClient

config = json.load(open('./config.json'))
client = MongoClient(config['mongo_url'])
db = client.test

data_sources = '1|3|8|9|11|12|105|170|172'

missing = db.pbdb_refs.find({ "classification_path": { "$exists": False }})

print "Searching through " + str(missing.count()) + " results "

for miss in missing:

  print miss['pid'] + " - has authorites entry?"
  auths = db.pbdb_authorities.find({"reference_no": miss['pid']})
  for auth in auths:
    print auth
    print "checking GNP for taxon - " + auth['taxon_name']

    title_tokens = auth['taxon_name'].replace('<i>', '').replace('</i>', '').replace('(', '').replace(')', '').replace(',', '').replace(':', '').split()

    for token in title_tokens:
      gnparser = requests.get('http://resolver.globalnames.org/name_resolvers.json?names=' + token + '&data_source_ids=' + data_sources + '&with_vernaculars&with_context=true')

      if 200 == gnparser.status_code:
        gnp_json = json.loads( gnparser.content )

        if 'data' in gnp_json:
          known_name = gnp_json['data'][0]['is_known_name']
          if known_name and 'results' in gnp_json['data'][0]:

            print " ++++ Found Classification Path for [" + miss['pid'] + "] - " + auth['taxon_name']
            classification_path = unidecode.unidecode( gnp_json['data'][0]['results'][0]['classification_path'] )

            # If results are found but classification path is empty. Just enter the name string
            if "" == classification_path:
              classification_path = gnp_json['data'][0]['results'][0]['name_string']

            print "Classification Path: " + classification_path
            db.pbdb_refs.update({"pid": miss['pid']}, { "$addToSet": { "classification_path": classification_path }})
