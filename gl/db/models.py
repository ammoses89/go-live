
from google.appengine.ext import ndb

class OutletProperty(ndb.Model):
    """Model that stores the release's outlet and corresponding status"""

    name = ndb.StringProperty(required=True)
    status = ndb.StringProperty(indexed=True, default="notlive")
    times_checked = ndb.IntegerProperty(default=0)

    created_at = ndb.DateTimeProperty(auto_now_add=True)
    updated_at = ndb.DateTimeProperty(auto_now=True)

    completed = ndb.BooleanProperty(indexed=True, default=False)
    removed = ndb.BooleanProperty(default=False)


class ReleaseModel(ndb.Model):
    """Model that stores release info"""


    album_id = ndb.StringProperty(indexed=True, required=True)
    upc = ndb.StringProperty(required=True)
    title = ndb.StringProperty(required=True)
    artist = ndb.StringProperty(required=True)

    created_at = ndb.DateTimeProperty(auto_now_add=True)
    updated_at = ndb.DateTimeProperty(auto_now=True)

    outlets = ndb.StructuredProperty(OutletProperty, repeated=True)

    emails = ndb.StringProperty(indexed=False, repeated=True)

    do_notify = ndb.BooleanProperty(default=False)

    @classmethod
    @ndb.tasklet
    def add_release_async(cls, upc, album_id, title, artist, outlets,
        emails=[]):

        release = ReleaseModel(
            album_id=album_id,
            upc=upc,
            title=title,
            artist=artist)

        outlet_props = []
        for outlet in outlets:
            outlet_props.append(
                OutletProperty(name=outlet)
            )

        release.outlets = outlets
        yield release.put_async()
        raise ndb.Return(release)


    @classmethod
    def query_for_album_id(cls, album_id):
        # TODO validate album_id
        return cls.query(cls.album_id==album_id)
