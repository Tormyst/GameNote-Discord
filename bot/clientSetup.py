import discord
from shlex import split
from .preferences import Preferences


def handle_write(c:discord.Client, message:discord.Message, command:list, pref:Preferences):
    if message.server and len(command) == 3:
        if(command[2] == "here"):
            toSet = message.channel
        elif len(message.channel_mentions) > 0 and message.channel_mentions[0].type == discord.ChannelType.text:
            toSet = message.channel_mentions[0]

        if not pref.addServerChannel(message.server, toSet):
            yield from c.send_message(message.channel, 'Something went wrong while saving the setting.')
        yield from c.send_message(message.channel, 'Ok, I will use {}'.format(toSet))


def handle_playing(c:discord.Client, message:discord.Message, command:list, pref:Preferences):
    if len(command) == 4:
        pref.addGameSaying(command[2], command[3])
        yield from c.send_message(message.channel, 'Done.')
    else:
        yield from c.send_message(message.channel, 'I don\'t get what you are telling me to do.  '
                                                   'Make sure to use quotation marks around the game name'
                                                   ' and the saying')


def handle_removeplaying(c: discord.Client, message: discord.Message, command: list, pref: Preferences):
    if len(command) == 4:
        if pref.rmGameSaying(command[2], command[3]):
            yield from c.send_message(message.channel, 'Removed.')
        else:
            yield from c.send_message(message.channel, 'Could not remove that.  Check that you wrote it right.')
    else:
        yield from c.send_message(message.channel, 'I don\'t get what you are telling me to do.  '
                                                   'Make sure to use quotation marks around the game name'
                                                   ' and the saying')


def handle_help(c:discord.Client, message:discord.Message, command:list, pref:Preferences):
    help_text = "All commands start with a mention of me, " \
               "the same way you talk to people who are as far as know not bots.\n" \
               "Commands:\n" \
               "\t➢ `write [here|#<channelname>]`\n" \
               "\t\tsets which channel I write to.\n" \
               "\t➢ `playing \"<game>\" \"<is playing text>\"`\n" \
               "\t\tReplaces \"is now playing\" with is playing text for a specific game.  " \
                "Randomly will select from all options given for that game. \n" \
                "\t➢ `removeplaying \"<game>\" \"<is playing text>\"`\n" \
                "\t\tRemoves the is playing text for that game indicated.\n" \
                "\t➢ `about`\n" \
               "\t\tPrints what I do."
    yield from c.send_message(message.channel, help_text)


def handle_about(c:discord.Client, message:discord.Message, command:list, pref:Preferences):
    aboutText = "Hello, I am a bot that will post a message whenever I detect a player starting up a game."
    yield from c.send_message(message.channel, aboutText)


def clientSetup(pref:Preferences):
    c = discord.Client()

    @c.async_event
    def on_message(message:discord.Message):
        if message.content.startswith(c.user.mention) and not message.author.bot:
            command = split(message.content)
            commandWord = command[1].lower()
            if commandWord == "write":
                yield from handle_write(c, message, command, pref)
            elif commandWord == "playing":
                yield from handle_playing(c, message, command, pref)
            elif commandWord == "removeplaying":
                yield from handle_removeplaying(c, message, command, pref)
            elif commandWord == "help":
                yield from handle_help(c, message, command, pref)
            elif commandWord == "about":
                yield from handle_about(c, message, command, pref)
            else:
                yield from c.send_message(message.channel, "I don't understand what you said.  Try asking for help with {} help".format(c.user.mention))

    @c.async_event
    def on_member_update(old:discord.Member, new:discord.Member):
        if new.game and old.game != new.game and not old.bot:
            sendOn = pref.getServerChannel(old.server)
            yield from c.send_message(sendOn, "{0} {1}.".format(new.name, pref.getGameSaying(new.game.name)))

    return c