import os
import pickle
from random import choice
from discord import Server, Channel

channelFile = "data/channelPref.dat"
gameFile = "data/gamePref.dat"

class Preferences:
    def __init__(self):
        if os.path.exists(channelFile):
            f = open(channelFile, 'rb')
            self.serverChannels = pickle.load(f)
            f.close()
        else:
            self.serverChannels = {}

        if os.path.exists(gameFile):
            f = open(gameFile, 'rb')
            self.gameSayings = pickle.load(f)
            f.close()
        else:
            self.gameSayings = {}

    def getServerChannel(self, s:Server) -> Channel:
        if s.id in self.serverChannels.keys():
            return s.get_channel(self.serverChannels[s.id])
        else:
            return s.default_channel

    def addServerChannel(self, s:Server, c:Channel) -> bool:
        retVal = True
        self.serverChannels[s.id] = c.id
        try:
            f = open(channelFile, 'wb+')
            pickle.dump(self.serverChannels, f)
        except IOError:
            retVal = False
        else:
            f.close()
        return retVal

    def getGameSaying(self, g):
        if g in self.gameSayings.keys() and len(self.gameSayings[g]) > 0:
            return choice(self.gameSayings[g])
        else:
            return "is now playing {}".format(g)

    def addGameSaying(self, g, saying):
        if g in self.gameSayings:
            self.gameSayings[g].append(saying)
        else:
            self.gameSayings[g] = [saying]
        retVal = True
        try:
            f = open(gameFile, 'wb+')
            pickle.dump(self.gameSayings, f)
        except IOError:
            retVal = False
        else:
            f.close()
        return retVal

    def rmGameSaying(self, g, saying):

        if g in self.gameSayings:
            try:
                self.gameSayings[g].remove(saying)
            except ValueError:
                return False
            retVal = True
            try:
                f = open(gameFile, 'wb+')
                pickle.dump(self.gameSayings, f)
            except IOError:
                retVal = False
            else:
                f.close()
            return retVal
        else:
            return False