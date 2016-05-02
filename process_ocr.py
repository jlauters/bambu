 #!/usr/bin/python

# Process OCR Blobs into meaningfull lookup documents
#
# author: @jlauters

import sys
import json
import utils
import requests
import editdistance
from pymongo import MongoClient
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

config = json.load(open('./config.json'))

# MongoDB Setup
client = MongoClient(config['mongo_url'])
db = client.test

# inits
search_name = sys.argv[1]
print "Searching for: " + search_name

vectorizer = CountVectorizer()


# Get iDigBio Records
def getSpecimens():
  idigbio = requests.get('https://search.idigbio.org/v2/search/records/?rq={"order":"' + search_name + '"}')
  if 200 == idigbio.status_code:
    idigbio_json = json.loads( idigbio.content )

    return idigbio_json['items']

#===================#
#     Get Data      #
#===================#

train_set = []
test_set  = [] 
records = db.pbdb_ocr.find({"found_by": search_name})
items = getSpecimens()

print "iDigBio Count: " + str(len(items))

for record in records:
  print "[" + record['oid'] + "] Title: " + record['title']
  train_set.append( record['ocr_text'] )
  test_set.append( record['ocr_text'] )

  vectorizer.fit(train_set)

  for test in test_set:
    #bow     = vectorizer.transform(test)
    smatrix = vectorizer.transform(test)
    tfidf = TfidfTransformer(norm="l2")
    tfidf.fit(smatrix)

    for item in items:
      term_match = 0
      matched_on = []
      specimen = utils.init_fields(item['data'])

      for term in vectorizer.vocabulary_:
        for key, value in specimen.iteritems():
          clean_term  = utils.normalize(term)
          clean_value = utils.normalize(value)
          dist        = editdistance.eval(clean_term, clean_value)

          if term == value or dist < 5:
            term_match += 1
            if key not in matched_on:
              matched_on.append(key)

    if term_match >= 10:
      print "specimen match"
      print ", ".join(matched_on)

      result = db.epandda_match.insert_one({"oid": record['oid'], "uuid": item['uuid']})
