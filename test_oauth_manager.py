import unittest
from oauth_manager import FacebookConnect, TwitterConnect


class TestFacebookConnect(unittest.TestCase):

    def setUp(self):
        self.base_url = 'https://graph.facebook.com/'
        self.redirect_uri = \
            'https://www.facebook.com/connect/login_success.html'
        self.params = {
            'scope': 'read_stream',
            'response_type': 'code',
            'redirect_uri': self.redirect_uri,
        }
        self.client_id = '452662148146137'
        self.secret = '1b4c1c4b744b4d69999a5a7cbcec12a7'
        self.facebook = FacebookConnect(self.client_id, self.secret)

    def test_authorize_url(self):
        """Should be able to get authorize_url"""
        auth_url = self.facebook.get_authorize_url(
            redirect_uri=self.redirect_uri)
        self.assertEqual(
            auth_url, 'https://graph.facebook.com/oauth/'
            'authorize?redirect_uri=https%3A%2F%2Fwww.facebook.com%2Fconnect'
            '%2Flogin_success.html&client_id=452662148146137')

    def test_session_testuser(self):
        access_token = self.facebook.get_access_token(self.redirect_uri)
        session = self.facebook.service.get_session(token=access_token)
        response = session.post(
            self.client_id + '/accounts/test-users/',
            params={
                'installed': True,
                'name': 'Fulano de Tal',
                'locale': 'en_US',
                'permissions': 'read_stream',
                'access_token': access_token
            })

        test_user = response.json()
        session = self.facebook.service.get_session(
            token=test_user['access_token'])
        test_user_info = session.get('me').json()
        self.assertEqual(test_user_info['first_name'], 'Fulano')


class TestTwitterConnect(unittest.TestCase):

    def setUp(self):
        self.consumer_key = 'PUJLMjntjYSFUF7A1uyCQ'
        self.consumer_secret = '2ir3CCD1zzWRb0ubCSwCY3OtzoO24PEPkhy1OXlckQ'
        self.twitter = TwitterConnect(self.consumer_key, self.consumer_secret)

    def test_shold_get_request_token(self):
        self.twitter.get_request_token()
        assert(self.twitter.request_token)

    def test_should_get_request_token_secret(self):
        self.twitter.get_request_token()
        assert(self.twitter.request_token_secret)

    def test_should_get_correct_login_url(self):
        base_url = 'https://api.twitter.com/oauth/authorize?oauth_token='
        self.twitter.get_request_token()
        url = self.twitter.get_authorize_url()
        self.assertEqual(url, base_url + self.twitter.request_token)

if __name__ == '__main__':
    unittest.main()
