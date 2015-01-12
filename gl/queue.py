from google.appengine.ext import taskqueue
from google.appengine.ext import ndb


class Release(ndb.Model):

    upc = ndb.StringProperty()

    created_at = ndb.DateTimeProperty(auto_now_add=True)

    updated_at = ndb.DateTimeProperty(auto_add=True)

    title = ndb.StringProperty()

    artist = ndb.StringProperty()

    is_up = ndb.BooleanProperty(default=False)

    retries = ndb.IntegerProperty(default=0)

    @classmethod
    def query_for_releases(cls, date_object):
        pass


