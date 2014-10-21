import tweepy
import logging


def login(consumer_key, consumer_secret, access_token, access_token_secret):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api


def get_since_id(api, screen_name, previous=10):
    timeline = api.user_timeline(screen_name=screen_name, count=previous+1)
    try:
        return timeline[-1].id
    except IndexError:
        return 1


def get_unique_statuses(api, screen_name, since_id, cache):
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
                url_count = cache.get(expanded_url, None)
                logger.info("%s - %s -- %s" % (s.id, expanded_url, url_count))
                if url_count is not None or 0:
                    cache.set(expanded_url, url_count+1)
                else:
                    stati.append(s)
                    cache.set(expanded_url, 1)
        if len(timeline) > 0:
            page += 1
        else:
            gather_results = False
    return stati
