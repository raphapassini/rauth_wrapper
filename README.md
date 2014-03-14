rauth-wrapper
=============

An wrapper around rauth to simplify the use of Facebook, Twitter and Google+ APIs

How to install
===============

```
git clone git@github.com:raphapassini/rauth_wrapper.git
cd /path/to/rauth_wrapper
pip install -r requirements.txt
```

How to use it
=============

The basic flow of Oauth is quite simple:
 - First you need a ID, SECRET and a REDIRECT_URL.
 - Then you have to redirect the user to authorize_url
 - When the user does/doesn't authorize your app he'll be redirect to your REDIRECT_URL
   and you'll be able to catch the access_token from the querystring
 - Getting the access_token enables you to access the API
 
In the lines bellow i tried to write a simple example of each service.


Facebook
--------

```python
from rauth_wrapper.oauth_manager import FacebookConnect

FB_CLIENT_ID = '1234'
FB_CLIENT_SECRET = '5678'
FB_REDIRECT_URI = 'http://localhost/authorize/'


def connect(request):
  """this function is called when user click to sigin with facebook"""
  facebook = FacebookConnect(FB_CLIENT_ID, FB_CLIENT_SECRET)
  auth_url = facebook.get_authorize_url(redirect_uri=FB_REDIRECT_URI)
  redirect(auth_url)
  
  
def authorize(request):
  """this function is called when user hits FB_REDIRECT_URL"""
  try:
    code = request.GET['code']
  except:
    raise Exception("Can't get code from url")
  
  facebook = FacebookConnect(FB_CLIENT_ID, FB_CLIENT_SECRET)
  session = facebook.get_session(code, FB_REDIRECT_URI)
  
  #print user info
  print session.get('me')
```

Google+
-------

```python
from rauth_wrapper.oauth_manager import GooglePlusConnect

G_CLIENT_ID = '1234'
G_CLIENT_SECRET = '5678'
G_REDIRECT_URI = 'http://localhost/authorize/'


def connect(request):
  """this function is called when user click to sigin with google+"""
  google = GooglePlusConnect(G_CLIENT_ID, G_CLIENT_SECRET)
  auth_url = google.get_authorize_url(redirect_uri=G_REDIRECT_URI)
  redirect(auth_url)
  
  
def authorize(request):
  """this function is called when user hits G_REDIRECT_URI"""
  try:
    code = request.GET['code']
  except:
    raise Exception("Can't get code from url")
  
  google = GooglePlusConnect(G_CLIENT_ID, G_CLIENT_SECRET)
  session = google.get_session(code, G_REDIRECT_URI)
  
  #print all the people that user know
  print session.get('people')
```

Twitter
-------

```python
from rauth_wrapper.oauth_manager import TwitterConnect

CONSUMER_KEY = '1234'
CONSUMER_SECRET = '5678'

def connect(request):
  """this function is called when user click to sigin with twitter"""
  twitter = TwitterConnect(CONSUMER_KEY, CONSUMER_SECRET)
  auth_url = twitter.get_request_token().get_authorize_url()
  redirect(auth_url)
  
  
def authorize(request):
  """this function is called when user hits twitter callback url"""
  try:
    oauth_verifier = request.GET['oauth_verifier']
  except:
    raise Exception("Can't get oauth_verifier from url")
  
  twitter = TwitterConnect(CONSUMER_KEY, CONSUMER_SECRET)
  session = twitter.get_session(oauth_verifier)
  
  #prints user twitter info
  session.get('account/verify_credentials')
```
