
from google.appengine.ext import ndb

class Account(ndb.Model):
    username = ndb.StringProperty()
    userid = ndb.IntegerProperty()
    # email = ndb.StringProperty()
    entries = ndb.IntegerProperty()
    # phone_no = ndb.StringProperty()

    @classmethod
    def query_users(cls,ancestor_key):
        return cls.query(ancestor = ancestor_key)



class Tables(ndb.Model):
	booked_by_id = ndb.IntegerProperty()
	booked_by_name = ndb.StringProperty()
	booked = ndb.BooleanProperty()
	max_occupancy = ndb.IntegerProperty()
	table_no = ndb.IntegerProperty()
	time_of_booking = ndb.TimeProperty()

	@classmethod
	def query_tables(cls,ancestor_key):
		return cls.query(ancestor = ancestor_key)
