import pymongo
from pymongo import MongoClient

DuplicateKeyError = pymongo.errors.DuplicateKeyError

client = MongoClient('localhost', 27017)

def get_db():
    db = client.go_live
    ensure_unique_index(db.releases)
    return db

def ensure_unique_index(coll):
    index_info = coll.index_information()
    if not "upc_index" in index_info.keys():
       coll.create_index("upc_index", unique=True, dropDups=True)

def get_collection(coll):
    db = get_conn()
    add_unique_index(coll)
    return db[coll]
