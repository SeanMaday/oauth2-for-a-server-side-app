#!/usr/bin/env python

import httplib2


from google.appengine.ext import webapp
import wsgiref.handlers
from google.appengine.api import users

from oauth2client.appengine import StorageByKeyName
from oauth2client.appengine import CredentialsProperty
from google.appengine.ext import db
from google.appengine.api import memcache

import simplejson as json

class Credentials(db.Model):
  credentials = CredentialsProperty()

class MyHandler(webapp.RequestHandler):
	def get(self):
		credentials = StorageByKeyName(Credentials, "key_for_credentials", 'credentials').get()
		PageOutput = ""
		PageOutput += "<br><br>"

		if not credentials or credentials.invalid or credentials.refresh_token is None:
			PageOutput += "Missing OAuth 2.0 Credentials"
		else:
			if credentials.refresh_token is not None:
				PageOutput += "This app has someone's " + str(len(credentials.refresh_token)) + " character refresh token on file!"
			else:
				PageOutput += "I can not find your refresh token!"
			PageOutput += "<br><br>"

			http = httplib2.Http()
			http = credentials.authorize(http)
			resp, content = http.request("https://www.googleapis.com/tasks/v1/users/@me/lists", "GET")

			ResultObj = json.loads(content)
			PageOutput += "The account authorizing this app has " + str(len(ResultObj['items'])) + " task list(s)."

		PageOutput += "<br><br><br>"
		PageOutput += "<a href='/oauth2authorize'>Authorize</a><br>"
		PageOutput += "<a href='/'>Check</a><br>"
		PageOutput += "<a href='/oauth2revoke'>Revoke</a><br>"
		self.response.out.write(PageOutput)

def main():
	app = webapp.WSGIApplication([(r'.*', MyHandler)], debug=True)
	wsgiref.handlers.CGIHandler().run(app)

if __name__ == "__main__":
	main()
