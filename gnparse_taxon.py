import json
import requests
import unidecode
from pymongo import MongoClient

config = json.load(open('./config.json'))
client = MongoClient(config['mongo_url'])
db = client.test

data_sources = '1|3|8|9|11|12|105|170|172'

records = db.pbdb_taxon_lookup.find({'classification_path': { '$eq': []}}).limit(100).skip(100)
for record in records:

  for sciname in record['genus']:
 
    gnparser = requests.get('http://resolver.globalnames.org/name_resolvers.json?names=' + sciname + '&data_source_ids=' + data_sources + '&with_vernaculars&with_context=true')
    if 200 == gnparser.status_code:
        gnp_json = json.loads( gnparser.content )

        known_name = gnp_json['data'][0]['is_known_name']
        print "[" + record['ref_no'] + "] - sciname: " + sciname + ' ==> is_known_name: ' + str( known_name )

        if known_name and 'results' in gnp_json['data'][0]:
            print gnp_json['data'][0]['results']

            for gn_result in gnp_json['data'][0]['results']:
              if gn_result['classification_path']:

                # Capture classification path
                classification_path = unidecode.unidecode( gn_result['classification_path'] )

            print "Updating Classification path -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-"
            print "Classification: " + classification_path
          
            db.pbdb_taxon_lookup.update({"ref_no": record['ref_no']}, { "$addToSet": { "classification_path": classification_path } })

            # Check if vernaculars and capture
            if gnp_json['data'][0]['results'][0]['vernaculars']:
 
              print "======= VERNACULARS FOUND ================"
              print gnp_json['data'][0]['results'][0]['vernaculars']

