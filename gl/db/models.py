
from google.appengine.ext import ndb


class Release(ndb.Model):


    album_id = ndb.StringProperty(indexed=True)

    created_at = ndb.DateTimeProperty(auto_now_add=True)
    updated_at = ndb.DateTimeProperty(auto_now=True)

    outlet_keys = ndb.KeyProperty(indexed=True, repeated=True)
    outlets = ndb.ComputedProperty(lambda self: self._get_outlet_names(),
        repeated=True)


    def _get_outlet_names(self):
        outlet_names = []
        for outlet_key in self.outlet_keys:
            outlet_name = outlet_key.string_id().split('-')[-1]
            outlet_names.append(outlet_name)
        return outlet_names



class Outlet(ndb.Model):

    status = ndb.StringProperty(indexed=True)

    created_at = ndb.DateTimeProperty(auto_now_add=True)
    updated_at = ndb.DateTimeProperty(auto_now=True)

    completed = ndb.BooleanProperty(index=True, default=False)

    removed = ndb.BooleanProperty(default=False)

    def make_key(cls, release_id, outlet_name):
        string_id = "%s-%s" % (release_id, outlet_name)
        return ndb.Key(cls._get_kind(), string_id)

