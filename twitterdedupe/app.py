import logging

import tweepy
import requests


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


def _key(screen_name, url):
    return "%s_%s" % (screen_name, url)


def _lengthen_url(url):
    try:
        r = requests.get(url)
        return r.url
    except Exception:
        return url


def consider_status(status, cache, cache_length=604800):
    """
    Looks at a status, compares it to a cache of known urls
    and text-only Tweets. Returns either the status, or None if
    the status has been seen before.
    """
    logger = logging.getLogger("twitterdedupe.consider_status")
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
    return None


def get_my_unique_statuses(api, since_id, cache, cache_length=604800):
    logger = logging.getLogger("twitterdedupe.get_unique_statuses")
    screen_name = api.me().screen_name
    logger.info("%s -- since %s" % (screen_name, since_id))

#    gather_results = True
    stati = []
    page = 1

    # By using home_timeline, that means the retweeter user
    # has to be following the source(s) they want deduped
    timeline = api.home_timeline(since_id=since_id, page=page, count=100)
    for s in timeline:
        for url in s.entities['urls']:
            expanded_url = _lengthen_url(url['expanded_url'])
            key = _key(screen_name, expanded_url)
            if cache.get(key)is None:
                stati.append(s)
                cache.set(key, 1, cache_length)
                logger.info("%s - %s" % (s.id, expanded_url))
        if len(s.entities['urls']) == 0:
            # Let text only tweets pass through
            # TODO: Add MD5 checking because maybe someone will make a noisy
            # text account
            result = consider_status(s, cache, cache_length)
            if result is not None:
                stati.append(result)
    return stati
