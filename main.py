"""
Built as a Google App Engine Demo for Cloud Saturday
"""

import webapp2
import jinja2
import os
from datetime import date
from google.appengine.ext import ndb
from google.appengine.api import users
from google.appengine.api import mail


class Choice(ndb.Model):
    """Lunch choice"""
    choice_text = ndb.StringProperty()
    user = ndb.StringProperty()
    create_date = ndb.DateProperty(auto_now_add=True)


class Main(webapp2.RequestHandler):

    def get(self):
        variables = {}

        today = Choice.query(Choice.create_date==date.today())
        variables['choices'] = today

        template = JINJA_ENVIRONMENT.get_template("templates/home.html")
        self.response.write(template.render(variables))


    def post(self):

        choice_text = self.request.get("choice")
        user = self.request.get("name")
        choice = Choice(choice_text=choice_text, user=user)
        choice.put()
        self.redirect("/")

class EmailCron(webapp2.RequestHandler):

    def get(self):
        todays_choices = Choice.query(Choice.create_date==date.today())
        body = "Hey There! Here are today's choices for lunch <br />"
        for choice in todays_choices:
            body += "Choice: %s by %s <br />" % (choice.choice_text, choice.user)

        mail.send_mail("lunch@cslunch.appspotmail.com", "alex@cloudbakers.com", "Lunch Orders for Today", html=body)




JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
    )


app = webapp2.WSGIApplication([
     ('/', Main),
     ('/email', EmailCron),
], debug=True)



