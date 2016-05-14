import os
import pickle
from discord import Server, Channel

channelFile = "../data/channelPref.dat"

class Preferences:
    def __init__(self):
        if os.path.exists(channelFile):
            f = open(channelFile, 'rb')
            self.serverChannels = pickle.load(f)
            f.close()
        else:
            self.serverChannels = {}

    def getServerChannel(self, s:Server) -> Channel:
        if s.id in self.serverChannels:
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

