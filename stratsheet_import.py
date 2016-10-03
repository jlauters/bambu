# Import Chrono / Litho Data from spreadsheet into MongoDB

import csv
import json
from pymongo import MongoClient

config = json.load(open('./config.json'))

client = MongoClient(config['mongo_url'])
db = client.test

# Cretaceous abbreviations
cretaceous_labels = [
  {"series": "upper", "stage_abbr": "MAA", "stage_full": "Maastrichtian", "years_ma": 72.1, "error_ma": 0.2},
  {"series": "upper", "stage_abbr": "CAM", "stage_full": "Campanian", "years_ma": 83.6, "error_ma": 0.2},
  {"series": "upper", "stage_abbr": "SAN", "stage_full": "Santonian", "years_ma": 86.3, "error_ma": 0.5},
  {"series": "upper", "stage_abbr": "CON", "stage_full": "Coniacian", "years_ma": 89.8, "error_ma": 0.3},
  {"series": "upper", "stage_abbr": "TUR", "stage_full": "Turonian", "years_ma": 93.9, "error_ma": 0.0},
  {"series": "upper", "stage_abbr": "CEN", "stage_full": "Cenomanian", "years_ma": 100.5, "error_ma": 0.0},
  {"series": "lower", "stage_abbr": "ALB", "stage_full": "Albian", "years_ma": 113.0, "error_ma": 0.0},
  {"series": "lower", "stage_abbr": "APT", "stage_full": "Aptian", "years_ma": 125.0, "error_ma": 0.0},
  {"series": "lower", "stage_abbr": "BAR", "stage_full": "Barremian", "years_ma": 129.4, "error_ma": 0.0},
  {"series": "lower", "stage_abbr": "HAU", "stage_full": "Hauterivian", "years_ma": 132.9, "error_ma": 0.0},
  {"series": "lower", "stage_abbr": "VAL", "stage_full": "Valanginian", "years_ma": 139.8, "error_ma": 0.0},
  {"series": "lower", "stage_abbr": "BER", "stage_full": "Berriasian", "years_ma": 145.0, "error_ma": 0.0}
]

with open('litho_by_state.csv', 'rb') as csvfile:
  stratreader = csv.reader(csvfile, delimiter=',')
  for row in stratreader:

    state_province = row[0]
    geo_abbr = row[1]
    geo_unit = []
    stage = []
    citations = []
    
    # Break apart Geo Units into Dict
    if "/" in row[2]:
      parts = row[2].split("/")
      for part in parts:
        geo_unit.append(part)
    else:
      geo_unit.append(row[2])

    # Do Lookup for Stage abbreviation
    # Break cross stage for full name lookup
    if "/" in row[3]: 
      parts = row[3].split("/")
      for part in parts:
        for cret in cretaceous_labels:
          if part == cret['stage_abbr']:
            stage.append(cret)
    elif "-" in row[3]:
      parts = row[3].split("-")
      for part in parts:
        for cret in cretaceous_labels:
          if part == cret['stage_abbr']:
            stage.append(cret)
    else:
      for cret in cretaceous_labels:
        if row[3] == cret['stage_abbr']:
          stage.append(cret)

    # Break Citations on ;
    if ";" in row[4]:
      parts = row[4].split(";")
      for part in parts:
        citations.append(part)
    else:
      citations.append(row[4])

    print "State/Province: " + state_province
    print "Geol Abbr: " + geo_abbr
    print "Geol Unit: " + ', '.join(map(str, geo_unit))
    print "Stage: " + ', '.join(map(str, stage))
    print "Citation: " + ', '.join(map(str, citations))

    result = db.strat_lookup.insert_one({"state_province": state_province, 
                                         "geo_abbr": geo_abbr,
                                         "geo_unit": geo_unit,
                                         "stage": stage,
                                         "citation": citations})
