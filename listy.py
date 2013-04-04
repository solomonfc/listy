import webapp2
import os

from google.appengine.api import users
from google.appengine.ext.webapp import template

from apiclient.discovery import build
from oauth2client.appengine import OAuth2Decorator

import settings

decorator = OAuth2Decorator(
	client_id=settings.CLIENT_ID,
	client_secret=settings.CLIENT_SECRET,
	scope=settings.SCOPE)

service = build('tasks', 'v1')

class MainHandler(webapp2.RequestHandler):

	@decorator.oauth_required
	def get(self):
		tasks = service.tasks().list(tasklist='@default').execute(http=decorator.http())

		template_values = {
			'tasks': tasks['items'],
		}

		path = os.path.join(os.path.dirname(__file__), 'tasks.html')
		self.response.out.write(template.render(path, template_values))

class MainPage(webapp2.RequestHandler):
	def get(self):

		template_values = {
				'url': "http://www.google.com.hk",
				'url_linktext': "Google HK",
		}

		path = os.path.join(os.path.dirname(__file__), 'index.html')
		self.response.out.write(template.render(path, template_values))

class Listy(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/plain'
		self.response.write('!!!Listy!!!')

app = webapp2.WSGIApplication([
			('/', MainHandler),
			('/page', MainPage), 
			("/listy", Listy),
			(decorator.callback_path, decorator.callback_handler())
	],debug=True)

def main():
	application.run()

if __name__ == "__main__":
	main()