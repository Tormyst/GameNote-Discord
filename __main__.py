import os
from bot.clientSetup import clientSetup
from bot.preferences import Preferences


def main():

    os.chdir(os.path.dirname(__file__))

    p = Preferences()
    c = clientSetup(p)

    f = open("data/token.txt", 'r')
    token = f.readline()[:-1]
    f.close()
    c.run(token)

main()