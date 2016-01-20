import discord
import yaml
import osu
import guessgame
import triviagame
import musicplayer
import chatemotes

# Loading configurations from config.yaml
with open('../configuration/config.yaml', 'r') as f:
    doc = yaml.load(f)

# TODO Add support for 64 bit as well
if not discord.opus.is_loaded():
    discord.opus.load_opus('../library/libopus/libopus-0.x86.dll')


class Bot(discord.Client):
    def __init__(self):
        super().__init__()
        self.player = None

    def is_playing(self):
        return self.player is not None and self.player.is_playing()

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.startswith('!help'):
            help_channel = doc['CHANNELS']['help_channel']
            await self.send_message(message.channel,
                                    'Hello {}'.format(message.author.mention)+', please visit <#' + str(help_channel) +
                                    '> for a complete list of commands')

        # Loading the CHAT EMOTES from chatemotes.py
        # TODO get more Chat Emotes
        await chatemotes.main(self, message)

        # Music Player codes---------------
        if message.content.startswith('!load'):
            await musicplayer.load(self, message)

        if message.content.startswith('!play '):
            await musicplayer.play(self, message)

        if message.content.startswith('!pause'):
            await musicplayer.pause(self, message)

        if message.content.startswith('!resume'):
            await musicplayer.resume(self, message)

        if message.content.startswith('!stop'):
            await musicplayer.stop(self, message)

        if message.content.startswith('!playlist'):
            await musicplayer.playlist(self, message)

        # GUESS GAME------------------------------
        if message.content.startswith('!guess'):
            # Game Status updating
            now_playing = discord.Game(name='Guessing Game')
            await self.change_status(game=now_playing, idle=False)
            # call guessgame.py module
            await guessgame.guess(self, message)
            # Game Status updating
            now_playing = discord.Game(name='')
            await self.change_status(game=now_playing, idle=False)

        # TRIVIA GAME----------------------------
        # TODO the strings are not compared correctly. Need to fix.
        if message.content.startswith('!quiz'):
            # Game Status updating
            now_playing = discord.Game(name='Trivia Quiz')
            await self.change_status(game=now_playing, idle=False)
            await triviagame.quiz(self, message)
            # Game Status updating
            now_playing = discord.Game(name='')
            await self.change_status(game=now_playing, idle=False)

        # OSU! API FUNCTIONS--------------------
        # TODO implement other osu!API Functions
        if message.content.startswith('!stats'):
            my_string = message.content
            # osu module
            await self.send_message(message.channel, osu.stats(my_string))

        if message.content.startswith('!top'):
            my_string = message.content
            await self.send_message(message.channel,
                                    'Fetching the requested data. Please wait...\n\n')
            # osu module
            await self.send_message(message.channel, osu.top(my_string))

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')
        # Game Status updating
        now_playing = discord.Game(name='type !help for help')
        await self.change_status(game=now_playing, idle=False)

# email id and password loaded from config.yaml
emaild = doc['DISCORD_LOGIN']['email']
passwordd = doc['DISCORD_LOGIN']['password']
bot = Bot()
bot.run(emaild, passwordd)
