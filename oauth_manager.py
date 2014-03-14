"""
The MIT License (MIT)

Copyright (c) 2014 Raphael Passini (raphapassini[at]gmail[dot]com)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""
from rauth import OAuth1Service, OAuth2Service


class BaseConnect(object):
    session = None
    service = None

    def __init__(self, client_id, secret, name, authorize_url,
                 access_token_url, base_url):
        self.service = OAuth2Service(
            client_id=client_id,
            client_secret=secret,
            name=name,
            authorize_url=authorize_url,
            access_token_url=access_token_url,
            base_url=base_url)

    def get_authorize_url(self, **kwargs):
        if not kwargs.get('redirect_uri'):
            raise Exception('You must provide a redirect_uri to this function')

        return self.service.get_authorize_url(**kwargs)

    def get_session(self, code, redirect_uri, **kwargs):
        if self.session:
            return self.session

        kwargs.update({'code': code, 'redirect_uri': redirect_uri})
        self.session = self.service.get_auth_session(data=kwargs)
        return self.session

    def get_access_token(self, redirect_uri):
        return self.service.get_access_token(
            params={
                'redirect_uri': redirect_uri,
                'grant_type': 'client_credentials',
            })


class TwitterConnect(BaseConnect):
    """
    Flow to authenticate a user:
        - get_request_token()
        - get_authorize_url()
        - redirects user to authorize_url and get the oauth_verifier in the
          callback
        - get_auth_session(oauth_verifier)

    You'll endup with a rauth.session.OAuth1Session and you can call
    anything in twitter api by doing:

    Eg:
        # get the info about logedin user
        session.get('account/verify_credentials.json')
    """
    access_token_url = 'https://api.twitter.com/oauth/access_token'
    authorize_url = 'https://api.twitter.com/oauth/authorize'
    request_token_url = 'https://api.twitter.com/oauth/request_token'
    base_url = 'https://api.twitter.com/1.1/'
    request_token = None

    def __init__(self, consumer_key, consumer_secret):
        self.service = OAuth1Service(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            name='twitter',
            access_token_url=self.access_token_url,
            authorize_url=self.authorize_url,
            request_token_url=self.request_token_url,
            base_url=self.base_url
        )

    def get_request_token(self):
        self.request_token, self.request_token_secret = \
            self.service.get_request_token()

    def get_authorize_url(self):
        if not self.request_token:
            raise Exception('You should call get_request_token first')
            return

        return self.service.get_authorize_url(self.request_token)

    def get_session(self, oauth_verifier):
        if not self.request_token:
            raise Exception('You should call get_request_token first')

        return self.service.get_auth_session(
            self.request_token, self.request_token_secret,
            params={'oauth_verifier': oauth_verifier})


class FacebookConnect(BaseConnect):
    """
    Flow to authenticate a user:
        - get_authorize_url()
        - Redirects user to this url, wait for callback and get the
          'code' param
        - get_session(code, redirect_uri)

     You'll endup with a rauth.session.OAuth2Session and you can use the
     api as this:
     # get the info about logedin user
     session.get('me')
    """

    name = 'facebook'
    authorize_url = 'https://graph.facebook.com/oauth/authorize'
    access_token_url = 'https://graph.facebook.com/oauth/access_token'
    base_url = 'https://graph.facebook.com/'

    def __init__(self, client_id, secret):
        super(FacebookConnect, self).__init__(
            client_id=client_id,
            secret=secret,
            name=self.name,
            authorize_url=self.authorize_url,
            access_token_url=self.access_token_url,
            base_url=self.base_url)


class GooglePlusConnect(BaseConnect):
    """
    Flow to authenticate a user:
        - get_authorize_url()
        - Redirects user to this url, wait for callback and get the
          'code' param
        - get_session(code, redirect_uri)

     You'll endup with a rauth.session.OAuth2Session and you can use the
     api as this:
     # get the info about logedin user
     google_plus_connect.get_userinfo(session)
    """
    name = 'google_plus'
    authorize_url = 'https://accounts.google.com/o/oauth2/auth'
    access_token_url = 'https://accounts.google.com/o/oauth2/token'
    base_url = 'https://www.googleapis.com/plus/v1/'

    def __init__(self, client_id, secret):
        super(GooglePlusConnect, self).__init__(
            client_id=client_id,
            secret=secret,
            name=self.name,
            authorize_url=self.authorize_url,
            access_token_url=self.access_token_url,
            base_url=self.base_url)

    def get_session(self, code, redirect_uri, *args, **kwargs):
        kwargs.update({
            'code': code,
            'redirect_uri': redirect_uri,
            'client_id': self.service.client_id,
            'client_secret': self.service.client_secret,
            'grant_type': 'authorization_code'
        })
        response = self.service.get_raw_access_token(data=kwargs)
        response = response.json()
        return self.service.get_session(response['access_token'])

    def get_userinfo(self, session):
        if not type(session) == 'rauth.session.OAuth2Session':
            raise Exception('Expect rauth.session.OAuth2Session object '
                            'instead got a %s' % (type(session)))
        return session.get(
            'https://www.googleapis.com/oauth2/v1/userinfo').json()
