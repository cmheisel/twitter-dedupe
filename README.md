twitter-dedupe
==============

![travis-ci status](https://api.travis-ci.org/cmheisel/twitter-dedupe.png?branch=master)

Python library to retweet unique links from noisy Twitter accounts.

My personal use case
------------------------
Say you follow a news outlet that tweets the same link multiple times in a day, or a week. Maybe they provide different images or headlines, but it's the same story, over and over again.

I'd rather follow @{newsoutlet}-light and have a link show up there only once every 7 days or so.


How to use
-------------
1. Set up a Twitter account, say @{newsoutlet}lite
2. As @{newsoutlet}lite Follow @newsoutlet
3. Get your Twitter Consumer Key, Consumer Key Secret, Access Key and Access Key Secret from http://dev.twitter.com
4. Set up some environment variables
    1. TWITTER_CONSUMER_KEY
    2. TWITTER_CONSUMER_SECRET
    3. TWITTER_ACCESS_TOKEN
    4. TWITTER_ACCESS_TOKEN_SECRET
    5. REDISTOGO_URL=redis://{user}:{pass}@{domain}:{port}
    6. TWITTER_SCREEN_NAME={newsoutlet}lite
    7. WAIT_INTERVAL=300 # Time to wait between polls, in seconds
    8. LOG_LEVEL=WARN # Or INFO, OR DEBUG, etc.
5. python bin/logonly.py
6. Now you have a deamon running that'll examine @{newsoutlet}lites home timeline, and log any tweets it would retwwet as @{newsoutlet}lite
7. If you're happy quiet bin/logonly.py
8. Noew run python bin/retweet.py # NOTE: Doesn't exist yet
