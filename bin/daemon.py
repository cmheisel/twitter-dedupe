import os

from twitterdedupe.daemons import ToggleDaemon

d = ToggleDaemon(os.environ)
d.run_forever()
