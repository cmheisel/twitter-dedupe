twitter-dedupe
==============

Python library to retweet unique links from noisy Twitter accounts.

My personal use case
------------------------
Say you follow a news outlet that tweets the same link multiple times in a day, or a week. Maybe they provide different images or headlines, but it's the same story, over and over again.

I'd rather follow @{newsoutlet}-light and have a link show up there only once every 7 days or so.

Notes on implementation plan
-------------------------------
* Watch account
    * Poll every N seconds?
* If text only, retweet via selected account
    * Defer deuping text only tweets if becomes a thing
* If link, and link not in one week cache
    * Retweet via selected account

Duplicate URLs
* May need to follow URLs to see if they redirect to circumvent URL shortners
* May need to strip query strings

Open questions to answer
---------------------------
* Good library for following an account or direct API access?
* Good library for retweeting?
* What info do I need from the noisy account to do retweets?
* Polling daemon or scheduled celery job? Or RQ?
* Memcache/Redis for cache? Or disk? Is there a nice pluggable cache backend I can use?

http://www.gavinj.net/2012/06/building-python-daemon-process.html
