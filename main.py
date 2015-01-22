"""
Built as a Google App Engine Demo for Cloud Saturday
"""

import webapp2
import jinja2
import os
from datetime import date
from google.appengine.ext import ndb
from google.appengine.api import users

class Choice(ndb.Model):
    """Lunch choice"""
    choice = ndb.StringProperty()
    user = ndb.StringProperty()
    create_date = ndb.DateProperty(auto_now_add=True)


class Main(webapp2.RequestHandler):

    def get(self):
        user = users.get_current_user()

        # redirect user if they are not logged into google
        if not user:
            return self.redirect(users.create_login_url(self.request.uri))

        variables = {}
        variables['user'] = user.nickname()

        today = Choice.query()
        variables['choices'] = today

        template = JINJA_ENVIRONMENT.get_template("templates/home.html")
        self.response.write(template.render(variables))


    def post(self):

        choice_text = self.request.get("choice")
        user = users.get_current_user().nickname()
        choice = Choice(choice=choice_text, user=user)
        choice.put()
        self.redirect("/")

class EmailCron(webapp2.RequestHandler):

    def post(self):
        pass




JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
    )


app = webapp2.WSGIApplication([
     ('/', Main)
], debug=True)



