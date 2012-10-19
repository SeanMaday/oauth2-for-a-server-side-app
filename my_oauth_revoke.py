#!/usr/bin/env python

import pickle
import httplib2

from google.appengine.ext import webapp
import wsgiref.handlers
from google.appengine.api import users
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.appengine import StorageByKeyName
from oauth2client.appengine import CredentialsProperty
from google.appengine.ext import db

def main():
	app = webapp.WSGIApplication([(r'.*', MyHandler)], debug=True)
	wsgiref.handlers.CGIHandler().run(app)

class Credentials(db.Model):
	credentials = CredentialsProperty()

class MyHandler(webapp.RequestHandler):
	def get(self):
		PageOutput = ""
		credentials = StorageByKeyName(Credentials, "key_for_credentials", 'credentials').get()
		StorageByKeyName(Credentials, "key_for_credentials", 'credentials').put(None)
		PageOutput = ""
		PageOutput += "<br><br>"
		if not credentials or credentials.invalid or credentials.refresh_token is None:
			PageOutput += "No Credentials"
			pass
		else:
				http = httplib2.Http()
				http = credentials.authorize(http)
				RevokeURL = "https://accounts.google.com/o/oauth2/revoke?token=" + str(credentials.refresh_token)
				resp, content = http.request(RevokeURL, "GET")

				PageOutput += "Bye. Bye. Bye."
		self.redirect("/")
if __name__ == "__main__":
	main()
