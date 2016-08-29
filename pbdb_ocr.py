#!/usr/bin/python

# PBDB OCR
# @author: Jon Lauters
# GET OCR for each pbdb ref in MongoDB Collection pbdb_refs

import re
import sys
import json
import utils
import requests
import unidecode
import editdistance
from pymongo import MongoClient

config = json.load(open('./config.json'))

# MongoDB Setup
client = MongoClient(config['mongo_url'])
db = client.test

# inits
insert_count = 0
bhl_base = config['bhl_base']
bhl_key  = config['bhl_key']

# functions from get_ocr.py

# Not sure if these are still needed

def badPBDB( oid ):
  insert_oid = oid.replace('ref:', '')
  result = db.bad_pbdb.insert_one({"oid": insert_oid})

def cleanBadPBDB( pbdb ):
  cleaned = []
  bad = db.bad_pbdb.find()

  for pb in pbdb:
    if pb['oid'] not in bad:
      cleaned.apend(pb)

  return cleaned

def cleanFound( pbdb ):
  cleaned   = []
  found_ids = []
  found = db.pbdb_ocr.find({}, {"ref.pid":1})
  for f in found:
    found_ids.append(f['ref']['pid'])

  for pb in pbdb:
    if pb['pid'] not in found_ids:
      cleaned.append(pb)
    
  return cleaned

# Check if publication is in BHL
def searchTitle( title ):

  if isinstance(title, (int, long)):
    srtitle = str(title)
  else:
    srtitle = unidecode.unidecode(title)

  bhl = requests.get(bhl_base + "?op=TitleSearchSimple&title=" + srtitle + "&apikey=" + bhl_key + "&format=json")
  if 200 == bhl.status_code:
    bhl_json = json.loads(bhl.content)

    bhl_title_count = len(bhl_json['Result'])
    print "BHL returned " + str(bhl_title_count) + " titles"

    return bhl_json['Result']

# Get Items for title
def searchTitleItems( title_id ):
  title_items = requests.get(bhl_base + "?op=GetTitleItems&titleid=" + str(title_id) + "&apikey=" + bhl_key + "&format=json")
  if 200 == title_items.status_code:
    items_json = json.loads(title_items.content)

    items_count = len(items_json['Result'])
    print "BHL returned " + str(items_count) + " items"

    return items_json['Result']

# Get Metadata for item
def searchMetadata( item_id ):
  params = "&pages=t&parts=t&ocr=t&apikey=" + bhl_key + "&format=json"
  meta_items = requests.get(bhl_base + "?op=GetItemMetadata&itemid=" + str(item_id) + params)
  if 200 == meta_items.status_code:

    try:
      meta_json  = json.loads(meta_items.content)
      meta_count = len(meta_json['Result'])
      print "BHL returned " + str(meta_count) + " meta items"
    except ValueError, e:
      return []
    return meta_json['Result']

  else:
    print "item_id: " + str(item_id) + " failed"
    return []

# ====================
#   Starting Script 
# ====================

references = db.pbdb_refs.find().limit(5000).skip(5000)

print "Pre Clean Count: " + str(references.count(with_limit_and_skip=True))

cleaned = cleanFound(references)
post_count = len(cleaned)
print "Post Clean Count: " + str(post_count)

for ref in cleaned:

  # PBDB Check for DOI
  doi = ref['doi'] 

  bhl_titles = searchTitle(ref['pubtitle'])
  if bhl_titles is None:
    bhl_titles = []
 

  for bhl_title in bhl_titles:

    print "Raw pubtitle: " + ref['pubtitle']

    # Normalize titles, get levdistance as second check
    pb_title = utils.normalize(ref['pubtitle'])
    bhl_full = utils.normalize(bhl_title['FullTitle'])
    dist = editdistance.eval(pb_title, bhl_full)

    if pb_title != bhl_full and dist > 10:

      # debugging in case of mistake
      print "DEBUG: Checking for title mistakes!!"
      print "pubtitle: " + pb_title
      print "BHL full: " + bhl_full
      print "LDist: "  + str(dist)

    else:

      print "Looking for title items!!"
 
      title_items = searchTitleItems(bhl_title['TitleID'])
      if title_items:
        for item in title_items:

          # Check Volume
          # TODO: normalize and LDIST?

          pb_vol  = ref['volume']
          if pb_vol is None:
            pb_vol  = ""

          pb_year = ref['pubyear']
          if pb_year is None:
            pb_year = ""

          bhl_vol           = item['Volume'].replace(" ", "")
          vol_pattern       = "v." + pb_vol + "(" + pb_year + ")"
          year_auth_pattern = ref['author1'] + "." + pb_year

          if vol_pattern not in bhl_vol and year_auth_pattern not in bhl_vol and pb_year not in bhl_vol:

            print "Items don't match"
            print "vol pattern: " + vol_pattern + ref['author1']
            print "BHL volume: " + item['Volume']

          else:

            if 'ItemID' in item and item['ItemID'] is not None:

              external_url = None
              meta = searchMetadata(item['ItemID'])
              if 'ExternalUrl' in meta:
                external_url = meta['ExternalUrl']
 
              if doi is None and external_url is not None:
                doi = external_url
                ref['doi'] = external_url

              add_to_db = False
              ocr_blob = ""

              if 'Pages' in meta: 
                for page in meta['Pages']:
                  stripped = utils.scanPage(page['OcrText'])
                  if stripped is not None:
                    ocr_blob += "\n" + stripped

                    # TODO: normalize, ldist, tokenize title and do TF-IDF?
                    if ref['title'][5:20].lower() in stripped.lower():
                      print "Found PBDB Title in OCR"
                      add_to_db = True
              else:
                print "Pages not in meta"
                print meta

              if add_to_db:
                insert_count += 1
                print "Added " + str(insert_count) + " OCR to DB"

                insert_oid = ref['pid']
                result = db.pbdb_ocr.insert_one({"ref": ref, "ocr_text": ocr_blob})             

