import hashlib
import webapp2
import jinja2
from google.appengine.api import users
import os
from mylist import MyList
from google.appengine.ext import ndb
from wordlist import WordList
from uanagram import UAnagram
from add import AddPage
from itertools import groupby


JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),extensions=['jinja2.ext.autoescape'],autoescape=True)

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        url = ''
        url_string = ''
        welcome = 'Welcome back'
        my_list = None
        d=[]
        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.uri)
            url_string = 'logout'
            key = ndb.Key('MyList', user.user_id())
            email=users.get_current_user().email()
            email=hashlib.sha1('%s' % (email)).hexdigest()
            word = self.request.get('searchword')
            lexicoword=''.join(k for k, g in groupby(sorted(word)))
            query=MyList.query(MyList.user_id==email)

            string8=None
            my_list1=None
            for i in query:
                if i.lexicographical in lexicoword:
                    if i.lexicographical==lexicoword:
                        pass
                    else:
                        string8=i.lexicographical
                        if string8==None:
                            pass
                        else:
                            key1=ndb.Key('MyList',string8+email)
                            my_list1=key1.get()
                            d.append(my_list1)
            key = ndb.Key('MyList', lexicoword+email)
            my_list = key.get()
        else:
            url = users.create_login_url(self.request.uri)
            url_string = 'login'

        template_values = {'url' : url,'url_string' : url_string,'user' : user,'welcome' : welcome,'my_list' : my_list,'my_list':my_list,'d':d}
        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render(template_values))



app = webapp2.WSGIApplication([('/', MainPage),
('/add',AddPage),
('/uanagram',UAnagram),
('/wordlist',WordList)],
debug=True)
