''' A library for LiveObject that queries Twitter for sentiment
analysis given several search terms'''

import twitter
import secret


api = twitter.Api(consumer_key=secret.consumer_key,
                  consumer_secret=secret.consumer_secret,
                  access_token_key=secret.access_token_key,
                  access_token_secret=secret.access_token_secret)

print api.VerifyCredentials()
