import discord
import yaml
import osu
import guessgame
import triviagame
import musicplayer
import chatemotes
import eightball

# Loading configurations from config.yaml
with open('../configuration/config.yaml', 'r') as f:
    doc = yaml.load(f)

# TODO Add support for 64 bit as well
if not discord.opus.is_loaded():
    discord.opus.load_opus('../library/libopus/libopus-0.x86.dll')

prefix = doc['BOT']['command_prefix']


class Bot(discord.Client):
    def __init__(self):
        super().__init__()
        self.player = None

    def is_playing(self):
        return self.player is not None and self.player.is_playing()

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.startswith(prefix+'help'):
            help_channel = doc['CHANNELS']['help_channel']
            await self.send_message(message.channel,
                                    'Hello {}'.format(message.author.mention)+', please visit <#' + help_channel +
                                    '> for a complete list of commands')

        # CHAT EMOTES
        # TODO get more Chat Emotes
        await chatemotes.main(self, message)

        # MUSIC PLAYER---------------
        if message.content.startswith(prefix+'load'):
            await musicplayer.load(self, message)

        if message.content.startswith(prefix+'play '):
            await musicplayer.play(self, message)

        if message.content.startswith(prefix+'pause'):
            await musicplayer.pause(self, message)

        if message.content.startswith(prefix+'resume'):
            await musicplayer.resume(self, message)

        if message.content.startswith(prefix+'stop'):
            await musicplayer.stop(self, message)

        if message.content.startswith(prefix+'playlist'):
            await musicplayer.playlist(self, message)

        # GUESS GAME------------------------------
        if message.content.startswith(prefix+'guess'):
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
        if message.content.startswith(prefix+'quiz'):
            # Game Status updating
            now_playing = discord.Game(name='Trivia Quiz')
            await self.change_status(game=now_playing, idle=False)
            await triviagame.quiz(self, message)
            # Game Status updating
            now_playing = discord.Game(name='')
            await self.change_status(game=now_playing, idle=False)

        # OSU! API--------------------
        # TODO implement other osu!API Functions
        if message.content.startswith(prefix+'stats'):
            my_string = message.content
            # osu module
            await self.send_message(message.channel, osu.stats(my_string))

        if message.content.startswith(prefix+'top'):
            my_string = message.content
            await self.send_message(message.channel,
                                    'Fetching the requested data. Please wait...\n\n')
            # osu module
            await self.send_message(message.channel, osu.top(my_string))

        # 8 BALL----------------------
        if message.content.startswith(prefix+'8ball'):
            await eightball.main(self, message)

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')
        # Game Status updating
        now_playing = discord.Game(name='type '+prefix+'help for help')
        await self.change_status(game=now_playing, idle=False)

# email id and password loaded from config.yaml
emaild = doc['DISCORD_LOGIN']['email']
passwordd = doc['DISCORD_LOGIN']['password']
bot = Bot()
bot.run(emaild, passwordd)
