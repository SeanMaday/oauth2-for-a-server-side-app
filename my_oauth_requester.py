#!/usr/bin/env python

import pickle


from google.appengine.ext import webapp
import wsgiref.handlers
from google.appengine.api import users
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.appengine import StorageByKeyName
from oauth2client.appengine import CredentialsProperty
from google.appengine.ext import db
from google.appengine.api import memcache

def main():
	app = webapp.WSGIApplication([(r'.*', MyHandler)], debug=True)
	wsgiref.handlers.CGIHandler().run(app)

class Credentials(db.Model):
	credentials = CredentialsProperty()

class MyHandler(webapp.RequestHandler):
	def get(self):

		MyHost = self.request.headers.get('host', 'no host')
		credentials = StorageByKeyName(Credentials, "key_for_credentials", 'credentials').get()
		PageOutput = ""

		if not credentials or credentials is None or credentials.invalid or credentials.refresh_token is None:
			user = users.get_current_user()

			flow = OAuth2WebServerFlow(
			# Visit the API Console to generate your client_id, client_secret and to register your redirect_uri
			client_id='[--PUT_YOUR_CLIENT_ID_HERE--]',
			client_secret='[--PUT_YOUR_CLIENT_SECRET_HERE--]',
			scope='https://www.googleapis.com/auth/tasks',
			access_type='offline',
			redirect_uri='http://' + MyHost + '/oauth2callback')
			callback = self.request.relative_url('/oauth2callback')

			authorize_url = flow.step1_get_authorize_url(callback)
			memcache.set(user.user_id(), pickle.dumps(flow))
			self.redirect(authorize_url)
		else:
			self.redirect("/")
  
if __name__ == "__main__":
	main()
