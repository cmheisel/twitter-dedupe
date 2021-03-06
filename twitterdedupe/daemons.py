import logging
import time

import redis
import tweepy


from twitterdedupe import login, get_my_unique_statuses, get_since_id
from twitterdedupe.caches import RedisCache


class Whitelist(logging.Filter):
    def __init__(self, *whitelist):
        self.whitelist = [logging.Filter(name) for name in whitelist]

    def filter(self, record):
        return any(f.filter(record) for f in self.whitelist)


class LoggingDaemon(object):
    """
    Base daemon that calls process_status passing it each unique Tweet.
    """

    def __init__(self, env):
        self.consumer_key = env['TWITTER_CONSUMER_KEY']
        self.consumer_secret = env['TWITTER_CONSUMER_SECRET']
        self.access_token = env['TWITTER_ACCESS_TOKEN']
        self.access_token_secret = env['TWITTER_ACCESS_TOKEN_SECRET']
        self.redis_url = env['REDISTOGO_URL']
        self.screen_name = env['TWITTER_SCREEN_NAME']
        self.interval = int(env['WAIT_INTERVAL'])
        self.log_level = getattr(logging, env['LOG_LEVEL'])
        self.do_retweet = bool(int(env.get('RETWEET', False)))
        self.instance = env.get('INSTANCE')

        self.redis = redis.from_url(self.redis_url)
        self.cache = RedisCache(self.redis, "cache|%s|" % self.screen_name)

        format_str = "%(levelname)s:%(name)s::%(message)s"
        log_prefix = "%s-%s:" % (self.instance, self.screen_name)
        format_str = log_prefix + format_str

        root_handler_name = self.screen_name
        logging.basicConfig(level=self.log_level, format=format_str)
        for handler in logging.root.handlers:
            handler.addFilter(Whitelist(root_handler_name, 'twitterdedupe'))
        self.logger = logging.getLogger(root_handler_name)

        self.api = login(self.consumer_key, self.consumer_secret,
                         self.access_token, self.access_token_secret)

    def process_status(self, status):
        pass

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
                    [self.process_status(s) for s in stati]
                    time.sleep(self.interval)
                except tweepy.error.TweepError, e:
                    self.logger.exception(str(e))
                    self.logger.info("Waiting %s more seconds" % self.interval)
                    time.sleep(self.interval)
        except KeyboardInterrupt:
            raise
        except Exception, e:
            self.logger.exception(str(e))


class ToggleDaemon(LoggingDaemon):
    """
    Daemon that will only log by default unless it the env
    passed to it contains RETWEET=1
    """

    def process_status(self, status):
        verb = "NOOP-RETWEET"
        if self.do_retweet:
            self.api.retweet(status.id)
            verb = "RETWEET"
        self.logger.info("%s: https://twitter.com/%s/status/%s" %
                         (verb, status.user.screen_name, status.id))
