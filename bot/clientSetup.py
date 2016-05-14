import discord
from preferences import Preferences

def handle_write(c:discord.Client, message:discord.Message, command:list, pref:Preferences):
    if message.server and len(command) == 3 and not message.author.bot:
        if(command[2] == "here"):
            toSet = message.channel
        elif len(message.channel_mentions) > 0 and message.channel_mentions[0].type == discord.ChannelType.text:
            toSet = message.channel_mentions[0]

        if not pref.addServerChannel(message.server, toSet):
            yield from c.send_message(message.channel, 'Something went wrong while saving the setting.')
        yield from c.send_message(message.channel, 'Ok, I will use {}'.format(toSet))

def handle_help(c:discord.Client, message:discord.Message, command:list, pref:Preferences):
    help_text = "All commands start with a mention of me, " \
               "the same way you talk to people who are as far as know not bots.\n" \
               "Commands:\n" \
               "\t➢ `write [here|#channelname]`\n" \
               "\t\tsets which channel I write to.\n" \
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
        if message.content.startswith("{}".format(c.user.mention)):
            print("Message for me")
            command = message.content.lower().split(" ")
            if command[1] == "write":
                yield from handle_write(c, message, command, pref)
            elif command[1] == "help":
                yield from handle_help(c, message, command, pref)
            elif command[1] == "about":
                yield from handle_about(c, message, command, pref)
            else:
                yield from c.send_message(message.channel, "I don't understand what you said.  Try asking for help with {} help".format(c.user.mention))


    @c.async_event
    def on_member_update(old:discord.Member, new:discord.Member):
        if new.game and old.game != new.game and old:
            sendOn = pref.getServerChannel(old.server)
            yield from c.send_message(sendOn, "{} is now playing {}.".format(new.name, new.game.name))

    return c