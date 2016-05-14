from clientSetup import clientSetup
from preferences import Preferences

p = Preferences()
c = clientSetup(p)

f = open("../data/token.txt", 'r')
token = f.read()
f.close()
c.run(token)