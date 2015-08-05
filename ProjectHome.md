This code will grant a server-side application OAUTH2 permissions using your Google account credentials. You must go through a specific workflow one time to grant permissions to your application. Once your application has acquired an OAUTH2 access token, any user can access the application using your credentials.
<br><br>
<h2>Background</h2>
<b><i>Why in the HELL would anyone want to do this?</i></b>
<br>
Great question! I developed this workflow because I wanted to build a public web service that leveraged the Google Prediction API. I developed and trained a model in the Prediction API that I needed to access in my web service application. To do this, I needed to allow my web app to make calls to the Prediction API using my Google credentials. I took great care to harden my app so that my account permissions could not be manipulated in nefarious ways!<br>
<br><br>
<h2>Working Demo</h2>
Check out <a href='http://oauth2-for-a-server-side-app.appspot.com/'>http://oauth2-for-a-server-side-app.appspot.com/</a>
<br><br>
<h2>Getting Started</h2>
<b>Step One</b>
<br>
Create a new API project in the Google API Console, and turn on a service to use in your project. For this demo app I have enabled the Tasks API and make a call against it in the sample code.<br>
<br>
<a href='https://code.google.com/apis/console/'>https://code.google.com/apis/console/</a>
<br><br>
<b>Step Two</b>
<br>
Create a 'Client ID for web applications' in the API console, and register the OAUTH redirect URIs you will use in your application. For testing in my local Google App Engine instance, I have registered this URI for my sample app:<br>
<br>
<a href='http://localhost:8085/oauth2callback'>http://localhost:8085/oauth2callback</a>
<br><br>
<b>Step Three</b>
<br>
Grab this software! The only major change you need to make is in the my_oauth_requester.py file. You will need to put in your own:<br>
<ul><li>client_id<br>
</li><li>client_secret<br>
</li><li>scope (this demo is set to access the Tasks API)<br>
<b>Step Four</b>
<br>
When you start to customize this code for your own use, you can begin by changing this line in the main.py file which is pointed to the Tasks API and returns all the authenticated user's task lists:<br>
<br>
resp, content = http.request("<a href='https://www.googleapis.com/tasks/v1/users/@me/lists'>https://www.googleapis.com/tasks/v1/users/@me/lists</a>", "GET")<br>
<br><br>
This approach uses the authorize() function of the Credentials class to apply necessary credential headers to all requests made by an httplib2.Http instance.