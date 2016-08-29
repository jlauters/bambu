#! /usr/bin/python
# Process OCR Data in Spark

#import sys
#import json
#import utils
#import requests
#import editdistance
from pymongo import MongoClient
from pyspark import SparkConf, SparkContext
#from sklearn.feature_extraction.text import CountVectorizer
#from sklearn.feature_extraction.text import TfidfTransformer

config = json.load(open('./config.json'))

conf = (SparkConf()
        .setMaster("local")
        .setAppName("epandda")
        .set("spark.executor.memory", "1g"))

sc = SparkContext(conf = conf)


# MongoDB Setup
client = MongoClient(config['mongo_url'])
db = client.test

ocr_records = db.pbdb_ocr.find()
records = sc.parallelize(ocr_records)
print records.first()
