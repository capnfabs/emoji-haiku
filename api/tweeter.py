import os
from typing import Any

import twitter

import haiku
from api.aws import LambdaContext


def _make_twitter_api_client() -> twitter.Api:
    return twitter.Api(
        consumer_key=os.environ['TWITTER_CONSUMER_KEY'],
        consumer_secret=os.environ['TWITTER_CONSUMER_SECRET'],
        access_token_key=os.environ['TWITTER_ACCESS_TOKEN_KEY'],
        access_token_secret=os.environ['TWITTER_ACCESS_TOKEN_SECRET'])


def tweet_handler(event: Any, context: LambdaContext) -> Any:
    """AWS Lambda entrypoint. Tweets a single haiku."""
    api = _make_twitter_api_client()
    emojis, text = haiku.formatted_haiku()
    api.PostUpdate(f'{emojis}\n{text}')


def test_print(event: Any, context: LambdaContext) -> Any:
    print('hello!')
    print(os.environ)
