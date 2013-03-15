import webapp2
import os
import settings

from google.appengine.api import users
from google.appengine.ext.webapp import template
from apiclient.discovery import build
from oauth2client.appengine import OAuth2Decorator

decorator = OAuth2Decorator(
	client_id=settings.CLIENT_ID,
	client_secret=settings.CLIENT_SECRET,
	scope=settings.SCOPE)

service = build('tasks', 'v1')

class TaskLists(webapp2.RequestHandler):

	@decorator.oauth_required
	def get(self):
		tasklists = service.tasklists().list().execute(http=decorator.http())
		path = os.path.join(os.path.dirname(__file__), 'taskList.html')
		self.response.out.write(template.render(path, tasklists))

class Tasks(webapp2.RequestHandler):
	
	@decorator.oauth_required
	def get(self):
		tasklistID = self.request.GET['id']
		
		tasklist = service.tasklists().get(tasklist=tasklistID).execute(http=decorator.http())
		tasks = service.tasks().list(tasklist=tasklistID).execute(http=decorator.http())
		
		values = { 
						'tasklist': tasklist, 
						'tasks': tasks['items']
					}

		path = os.path.join(os.path.dirname(__file__), 'tasks.html')
		self.response.out.write(template.render(path, values))

app = webapp2.WSGIApplication([
			('/', TaskLists),
			('/tasks', Tasks),
			(decorator.callback_path, decorator.callback_handler())
	],debug=True)

def main():
	application.run()

if __name__ == "__main__":
	main()