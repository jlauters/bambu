#!/usr/bin/python

# Get OCR
#
# @author: Jon Lauters
#
# Cmd Line Args: arg1( search_name )

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
pbdb_titles = []
insert_count = 0
bhl_base = config['bhl_base']
bhl_key  = config['bhl_key']

search_name = sys.argv[1]

print "Searching for: " + search_name

def badPBDB( oid ):
  insert_oid = oid.replace('ref:', '')
  result = db.bad_pbdb.insert_one({"oid": insert_oid})

def cleanBadPBDB( pbdb ):
  cleaned = []
  bad = db.bad_pbdb.find()

  for pb in pbdb:
    if pb['oid'] not in bad:
      cleaned.append(pb)

  return cleaned

# Get Biblio References from PBDB
def getPubs( base_name ):
  pbdb = requests.get('https://paleobiodb.org/data1.2/taxa/refs.json?base_name=' + base_name)
  if 200 == pbdb.status_code:
    pbdb_json = json.loads( pbdb.content )
   
    cleaned = cleanBadPBDB(pbdb_json['records'])
    pbdb_count = len(cleaned)
    print "PBDB returned " + str(pbdb_count) + " clean records"

    return cleaned

# Check if Publication is in BHL
def searchTitle( title ):

  if isinstance(title, (int, long)):
    srtitle = str(title)
  else:
    srtitle = unidecode.unidecode(title)

  bhl = requests.get(bhl_base + "?op=TitleSearchSimple&title=" + srtitle + "&apikey=" + bhl_key + "&format=json")
  if 200 == bhl.status_code:
    bhl_json = json.loads( bhl.content )

    bhl_title_count = len(bhl_json['Result'])
    print "BHL returned " + str(bhl_title_count) + " titles"

    return bhl_json['Result']

# Get Items for Title
def searchTitleItems( title_id ):
  title_items = requests.get(bhl_base + "?op=GetTitleItems&title_id=" + str(title_id) + "&apikey=" + bhl_key + "&format=json")
  if 200 == title_items.status_code:
    items_json = json.loads( title_items.content )

    items_count = len(items_json['Result'])
    print "BHL returned " + str(items_count) + " items"

    return items_json['Result']

# Get Metadata for item
def searchMetadata( item_id ):
  params = "&pages=t&parts=t&ocr=t&apikey=" + bhl_key + "&format=json"
  meta_items = requests.get(bhl_base + "?op=GetItemMetadata&itemid=" + str(item_id) + params)
  if 200 == meta_items.status_code:
    meta_json = json.loads( meta_items.content )
  
    meta_count = len(meta_json['Result'])
    print "BHL returned " + str(meta_count) + " meta items"

    return meta_json['Result']

#================
#  Script Start
#===============

pubs = getPubs(search_name)
for pb in pubs:

  # PBDB Check for DOI
  doi = pb['doi'] if 'doi' in pb else ""

  # Check for required fields
  if "tit" not in pb or "pbt" not in pb:
    badPBDB(pb['oid'])
  else:
    bhl_titles = searchTitle(pb['pbt'])
    for bhl_title in bhl_titles:
 
      # Normalize titles, get levdistance as second check
      pb_title = utils.normalize(pb['pbt'])
      bhl_full = utils.normalize(bhl_title['FullTitle'])
      dist = editdistance.eval(pb_title, bhl_full)

      if pb_title != bhl_full and dist > 10:

        # dump in case of dumb mistake
        print "PBT: " + pb_title
        print "BHL Full: " + bhl_full
        print "LDist: " + str(dist)

      else:
    
        title_items = searchTitleItems(bhl_title['TitleID'])
        if title_items:
          for item in title_items:
     
            # Check volume
            pb_vol            = pb['vol'] if 'vol' in pb else ""
            pby               = pb['pby'] if 'pby' in pb else ""
            bhl_vol           = item['Volume'].replace(" ", "")
            vol_pattern       = "v." + pb_vol + "(" + pby + ")"
            year_auth_pattern = pb['al1'] + "." + pby

            if vol_pattern not in bhl_vol and year_auth_pattern not in bhl_vol and pby not in bhl_vol:

              print "Items don't match"
              print "vol pattern: " + vol_pattern + pb['al1']
              print "BHL volume: " + item['Volume']

            else:

              meta = searchMetadata(item['ItemID'])
              external_url = meta['ExternalUrl']

              if doi is None and external_url is not None:
                doi = external_url

              add_to_db = False
              ocr_blob = ""
          
              for page in meta['Pages']:
                stripped = utils.scanPage(page['OcrText'])
                if stripped is not None:
                  ocr_blob += "\n" + stripped

                  if pb['tit'][5:20].lower() in stripped.lower():
                    print "Found PBDB Title in OCR"
                    add_to_db = True

              if add_to_db:
                insert_count += 1
                print "Added " + str(insert_count) + " Ocr to DB"

                insert_oid = pb['oid'].replace('ref:', '');
                result = db.pbdb_ocr.insert_one({"oid": insert_oid,
                                               "title" : pb['tit'],
                                               "found_by": search_name,
                                               "doi": doi,
                                               "ocr_text": ocr_blob})
