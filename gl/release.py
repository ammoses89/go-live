import datetime
from db import mongo
from bson.objectid import ObjectId

class Release(object):
    """This class represents the Release data object stored in mongo"""

    def __init__(self, upc, created_at, updated_at, is_up=False):
        self.upc = upc
        self.created_at = created_at
        self.updated_at = updated_at
        self.is_up = is_up

    def insert(self):
        release_dict = self.to_dict()
        db = mongo.get_db()
        releases = db.releases
        release_id = releases.insert(release_dict)
        return release_id

    @classmethod
    def get(cls, _id):
        db = mongo.get_db()
        result = db.releases.find_one({"_id": ObjectId(_id)})
        result.pop('_id')
        if not result:
            return None
        release = cls(**result)
        return release

    def to_dict(self):
        release_dict = {
          "upc" : self.upc,
          "created_at": self.created_at,
          "updated_at": self.updated_at,
          "is_up": self.is_up
        }
        return release_dict


class Releases(object):
     """This class represents multiple Releases and will be used for
        querying
     """
     @classmethod
     def query(cls, params_dict):
         db = mongo.get_db()
         results = db.releases.find(params_dict)
         print "%s results queried" % (results.count())
         releases = []
         for result in results:
            result.pop('_id')
            release = Release(**result)
            releases.append(release)
         return releases

     @classmethod
     def clear(cls):
         db = mongo.get_db()
         db.releases.remove()
