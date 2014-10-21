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


def lengthen_url(url):
    try:
        r = requests.get(url)
        return r.url
    except Exception:
        return url


def get_unique_statuses(api, screen_name, since_id, cache, cache_length=604800):
    logger = logging.getLogger("twitterdedupe.get_unique_statuses")
    logger.debug("%s -- since %s" % (screen_name, since_id))

    gather_results = True
    stati = []
    page = 1

    while gather_results:
        timeline = api.user_timeline(screen_name=screen_name, since_id=since_id, page=page)
        for s in timeline:
            for url in s.entities['urls']:
                expanded_url = lengthen_url(url['expanded_url'])
                key = _key(screen_name, expanded_url)
                if cache.get(key)is None:
                    stati.append(s)
                    cache.set(key, 1, cache_length)
                    logger.info("%s - %s" % (s.id, expanded_url))
            if len(s.entities['urls']) == 0:
                # Let text only tweets pass through
                # TODO: Add MD5 checking because maybe someone will make a noisy
                # text account
                key = _key(screen_name, hash(s.text))
                if cache.get(key) is None:
                    stati.append(s)
                    cache.set(key, 1, cache_length)
                    logger.info("%s - %s" % (s.id, s.text[:25]))

        if len(timeline) > 0:
            page += 1
        else:
            gather_results = False
    return stati
