from google.appengine.ext import ndb
from google.appengine.api import users
class MyList(ndb.Model):
    list_of_words = ndb.StringProperty(repeated=True)
    lexicographical = ndb.StringProperty()
    user_id = ndb.StringProperty()
    word_count =ndb.IntegerProperty()
    letter_count=ndb.IntegerProperty()
