import webapp2
import os

from google.appengine.api import users
from google.appengine.ext.webapp import template

class MainPage(webapp2.RequestHandler):
	def get(self):

		user = users.get_current_user()

		if user:
			self.response.headers['Content-Type'] = 'text/plain'
			self.response.out.write('Hello, ' + user.nickname())
		else:
			self.redirect(users.create_login_url(self.request.uri))

class Listy(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/plain'
		self.response.write('!!!Listy!!!')

app = webapp2.WSGIApplication([
		('/', MainPage), 
		("/listy", Listy)
	],debug=True)

def main():
	application.run()

if __name__ == "__main__":
	main()