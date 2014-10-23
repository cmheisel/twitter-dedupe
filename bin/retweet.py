import os

from twitterdedupe.daemons import RetweetDaemon

d = RetweetDaemon(os.environ)
d.run_forever()
