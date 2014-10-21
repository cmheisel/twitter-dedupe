import tweepy
import logging


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
                expanded_url = url['expanded_url']
                key = _key(screen_name, expanded_url)
                url_count = cache.get(key, None)
                logger.info("%s - %s -- %s" % (s.id, expanded_url, url_count))
                if url_count is None:
                    stati.append(s)
                    cache.set(key, 1, cache_length)
        if len(timeline) > 0:
            page += 1
        else:
            gather_results = False
    return stati
