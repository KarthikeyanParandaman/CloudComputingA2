import hashlib
import webapp2
import jinja2
from google.appengine.api import users
import os
from mylist import MyList
from google.appengine.ext import ndb

JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),extensions=['jinja2.ext.autoescape'],autoescape=True)

class AddPage(webapp2.RequestHandler):
    def post(self):
            self.response.headers['Content-Type'] = 'text/html'
            user = users.get_current_user()
            newword = self.request.get('addword')
            lexico_order=''.join(sorted(set(newword)))
            userid=users.get_current_user().email()
            userid = hashlib.sha1('%s' % (userid)).hexdigest()
            key = ndb.Key('MyList', lexico_order+userid)
            my_list = key.get()
            if my_list==None:
                my_list=MyList(id=lexico_order+userid)
                my_list.put()
            key = ndb.Key('MyList', lexico_order+userid)
            my_list = key.get()
            action=self.request.get('button')
            if action == 'Submit':
                string = self.request.get('addword')
                if string == None or string == '':
                    self.redirect('/')
                    return
                my_list.list_of_words.append(newword)
                my_list.lexicographical=lexico_order
                my_list.word_count=len(my_list.list_of_words)
                my_list.letter_count=len(my_list.lexicographical)
                my_list.user_id=userid
            my_list.put()
            self.redirect('/add')
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        template_values = {}
        template = JINJA_ENVIRONMENT.get_template('add.html')
        self.response.write(template.render(template_values))
