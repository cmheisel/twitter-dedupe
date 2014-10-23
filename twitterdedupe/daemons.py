import logging
import time

import redis
import tweepy


from twitterdedupe import login, get_my_unique_statuses, get_since_id
from twitterdedupe.caches import RedisCache


class LoggingOnlyDaemon(object):
    """
    Daemon that will only log unique tweets, DOES NOT RETWEET
    Useful for testing.
    """

    def __init__(self, env):
        self.consumer_key = env['TWITTER_CONSUMER_KEY']
        self.consumer_secret = env['TWITTER_ONSUMER_SECRET']
        self.access_token = env['TWITTER_ACCESS_TOKEN']
        self.access_token_secret = env['TWITTER_ACCESS_TOKEN_SECRET']
        self.redis_url = env['REDISTOGO_URL']
        self.screen_name = env['TWITTER_SCREEN_NAME']
        self.interval = env['WAIT_INTERVAL']
        self.log_level = getattr(logging, env['LOG_LEVEL'])

        self.redis = redis.from_url(self.redis_url)
        self.cache = RedisCache(redis, "cache|%s|" % self.screen_name)

        logging.basicConfig(level=self.log_level)
        for handler in logging.root.handlers:
            handler.addFilter('twitterdedupe')
        self.logger = logging.getLogger(self.screen_name)

        self.api = login(self.consumer_key, self.consumer_secret,
                         self.access_token, self.access_token_secret)

    def run_forever(self):
        try:
            start_id = get_since_id(self.api, self.api.me().screen_name)
            while True:
                try:
                    stati = get_my_unique_statuses(self.api, since_id=start_id, cache=self.cache)
                    self.logger.info("Unique urls: %s" % len(stati))
                    try:
                        start_id = stati[0].id
                    except IndexError:
                        pass
                    time.sleep(self.interval)
                except tweepy.error.TweepError, e:
                    self.logger.exception(str(e))
                    self.logger.info("Waiting %s more seconds" % self.interval)
                    time.sleep(self.interval)
        except KeyboardInterrupt:
            raise
        except Exception, e:
            self.logger.exception(str(e))
