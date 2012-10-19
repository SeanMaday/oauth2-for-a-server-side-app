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
		try:
			user = users.get_current_user()
			flow = pickle.loads(memcache.get(user.user_id()))
			if flow:
				credentials = flow.step2_exchange(self.request.params)
				StorageByKeyName(Credentials, "key_for_credentials", 'credentials').put(credentials)
			else:
				pass
		except:
			pass
		self.redirect("/")
if __name__ == "__main__":
	main()
