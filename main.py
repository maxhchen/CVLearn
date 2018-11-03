import webapp2
import jinja2
import os
from google.appengine.ext import ndb

env = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=["jinja2.ext.autoescape"],
    autoescape=True
)

class Message(ndb.Model):
    name = ndb.StringProperty()
    content = ndb.StringProperty()
    date_time = ndb.DateTimeProperty(auto_now_add = True)

class Main(webapp2.RequestHandler):
    def get(self):
        # 1. get info from user request
        # 2. Read from or write to database
        message_query = Message.query()
        message_query = message_query.order(-Message.date_time)
        messages = message_query.fetch()

        # 3. Render a responss
        templateVars = {
            "messages" : messages,
        }
        template = env.get_template("templates/main.html")
        self.response.write(template.render(templateVars))

    def post(self):
        # 1. get info from user request
        name = self.request.get("name")
        content = self.request.get("content")

        # 2. Read from or write to database
        message = Message(name = name, content = content)
        message.put()

        # 3. Render a responss
        self.redirect("/")

app = webapp2.WSGIApplication([
    ('/', Main),
], debug=True)
