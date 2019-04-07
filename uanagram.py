import hashlib
import webapp2
import jinja2
from google.appengine.api import users
import os
from mylist import MyList
from google.appengine.ext import ndb

JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),extensions=['jinja2.ext.autoescape'],autoescape=True)

class UAnagram(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        userid=users.get_current_user().email()
        userid = hashlib.sha1('%s' % (userid)).hexdigest()
        query=MyList.query(MyList.user_id==userid)
        template_values = {'query':query}
        template = JINJA_ENVIRONMENT.get_template('uanagram.html')
        self.response.write(template.render(template_values))
