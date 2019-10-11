import twitter
from .config import CONSUMER_KEY, CONSUMER_SECRET


class twitter_api:

    def request_token(self, hosturl, token_filename=None, open_browser=True):
        oc = hosturl + 'oauth_callback'
        tw = twitter.Twitter(
            auth=twitter.OAuth('', '', CONSUMER_KEY, CONSUMER_SECRET),
            format='', api_version=None)
        a = tw.oauth.request_token(oauth_callback=oc)
        oauth_token, oauth_secret = self.parse_oauth_tokens(
            a)

        oauth_url = ('https://api.twitter.com/oauth/authenticate?'
                     + 'oauth_token=' + oauth_token)
        return oauth_url, oauth_token, oauth_secret

    def get_oauth_token(self, oauth_token, oauth_secret, oauth_verifier):
        tw = twitter.Twitter(
            auth=twitter.OAuth(
                oauth_token, oauth_secret,
                CONSUMER_KEY, CONSUMER_SECRET),
            format='', api_version=None)
        oauth_token, oauth_secret = self.parse_oauth_tokens(
            tw.oauth.access_token(oauth_verifier=oauth_verifier))
        return oauth_token, oauth_secret

    def parse_oauth_tokens(self, result):
        for r in result.split('&'):
            k, v = r.split('=')
            if k == 'oauth_token':
                oauth_token = v
            elif k == 'oauth_token_secret':
                oauth_token_secret = v
        return oauth_token, oauth_token_secret

    def login_twitter_oauth(self, oauth_token, oauth_secret):
        self.api = twitter.Twitter(
            auth=twitter.OAuth(oauth_token, oauth_secret,
                               CONSUMER_KEY, CONSUMER_SECRET))
# end of class twitter_api
