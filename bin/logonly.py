import os

from twitterdedupe.daemons import LoggingOnlyDaemon

d = LoggingOnlyDaemon(os.environ)
d.run_forever()
