import hashlib
import webapp2
import jinja2
from google.appengine.api import users
import os
from mylist import MyList
from google.appengine.ext import ndb

JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),extensions=['jinja2.ext.autoescape'],autoescape=True)

class WordList(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        template_values = {}
        template = JINJA_ENVIRONMENT.get_template('wordlist.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        userid = users.get_current_user().email()
        userid = hashlib.sha1('%s' % (userid)).hexdigest()
        textfile = self.request.get("myFile")
        textfile = textfile.split()
        for x in textfile:
            line=''.join(sorted(set(x)))
            key = ndb.Key('MyList', line+userid)
            my_list = key.get()
            if my_list==None:
                my_list=MyList(id=line+userid)
                my_list.put()
            key = ndb.Key('MyList', line+userid)
            my_list = key.get()
            my_list.list_of_words.append(x)
            my_list.lexicographical=line
            my_list.word_count=len(my_list.list_of_words)
            my_list.letter_count=len(my_list.lexicographical)
            my_list.user_id=userid
            my_list.put()
        self.redirect('/')
