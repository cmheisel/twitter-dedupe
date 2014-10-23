import logging

import tweepy
import requests

from urlparse import urlsplit, urlunsplit


def login(consumer_key, consumer_secret, access_token, access_token_secret):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api


def get_since_id(api, screen_name):
    timeline = api.user_timeline(screen_name=screen_name)
    try:
        return timeline[-1].id
    except IndexError:
        return 1


def lengthen_url(url, reqlib=None):
    if reqlib is None:
        reqlib = requests
    try:
        r = reqlib.get(url)
        url = r.url
    except Exception:
        url = url

    # Ditch tracking query strings
    parts = urlsplit(url)
    parts = (parts[0], parts[1], parts[2], "", parts[4])
    return urlunsplit(parts)


def consider_status(status, cache, cache_length=604800, expand_fn=None):
    """
    Looks at a status, compares it to a cache of known urls
    and text-only Tweets. Returns either the status, or None if
    the status has been seen before.
    """
    logger = logging.getLogger("twitterdedupe.consider_status")
    if expand_fn is None:
        expand_fn = lengthen_url
    if len(status.entities['urls']) == 0:
        # Hey there's only text here
        key = str(hash("%s.%s" % (status.user.screen_name, status.text)))
        if cache.get(key) is None:
            logger.info("CACHE.MISS: %s.%s - %s" % (
                        status.user.screen_name,
                        status.id,
                        status.text
                        ))
            cache.set(key, 1, cache_length)
            return status
    else:
        # WE GOT LINKSIGN!!!
        url = status.entities['urls'][0]['expanded_url']
        expanded_url = expand_fn(url)
        key = expanded_url
        if cache.get(key) is None:
            logger.info("CACHE.MISS: %s.%s - %s" % (status.user.screen_name,
                        status.id, expanded_url))
            cache.set(key, 1, cache_length)
            return status
    return None


def get_my_unique_statuses(api, since_id, cache,
                           cache_length=604800, expand_fn=None):
    logger = logging.getLogger("twitterdedupe.get_unique_statuses")
    screen_name = api.me().screen_name
    logger.info("%s -- since %s" % (screen_name, since_id))

    stati = []

    # By using home_timeline, that means the retweeter user
    # has to be following the source(s) they want deduped
    timeline = api.home_timeline(since_id=since_id, page=1, count=100)
    for s in timeline:
        result = consider_status(s, cache, cache_length, expand_fn)
        if result is not None:
            stati.append(result)
    return stati
