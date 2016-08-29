# Import json file into MongoDB

import sys
import json
import utils
from pymongo import MongoClient
from pprint import pprint

config = json.load(open('./config.json'))

# MongoDB Setup
client = MongoClient(config['mongo_url'])
db = client.test

data_file = json.load(open('./pbdb_occurrences.json'))
#pprint(data_file);

for obj in data_file:
  print "object"
  pprint(obj)

  result = db.pbdb_occurrences.insert_one(obj)
