import discord
import yaml
import osu
import guessgame
import triviagame
import musicplayer
import chatemotes
import eightball

try:
    # Loading configurations from config.yaml
    with open('../configuration/config.yaml', 'r') as f:
        doc = yaml.load(f)
except FileNotFoundError:
    print('The config.yaml file was not found inside the configuration folder.' +
          '\n Make sure the file is present and run the bot again.')
    quit()

prefix = doc['BOT']['command_prefix']
if prefix is None:
    print('Prefix value cant be left empty and must be within single quotes.')
    quit()

try:
    # TODO Add support for 64 bit as well
    if not discord.opus.is_loaded():
        discord.opus.load_opus('../library/libopus/libopus-0.x86.dll')
except FileNotFoundError:
    print('The opus library file could not be found.' +
          '\nMake sure the file is present and run the bot again.')
    quit()


class Bot(discord.Client):
    def __init__(self):
        super().__init__()
        self.player = None

    def is_playing(self):
        return self.player is not None and self.player.is_playing()

    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content.startswith(prefix + 'help'):
            help_channel = doc['CHANNELS']['help_channel']
            # NOTE:- If help channel id is wrong then discord will display it as #deleted-channel
            await self.send_message(message.channel,
                                    'Hello {}'.format(message.author.mention) + ', please visit <#' + help_channel +
                                    '> for a complete list of commands')

        # CHAT EMOTES
        # TODO get more Chat Emotes
        await chatemotes.main(self, message)

        # MUSIC PLAYER---------------
        if message.content.startswith(prefix + 'load'):
            await musicplayer.load(self, message)

        if message.content.startswith(prefix + 'play '):
            await musicplayer.play(self, message)

        if message.content.startswith(prefix + 'pause'):
            await musicplayer.pause(self, message)

        if message.content.startswith(prefix + 'resume'):
            await musicplayer.resume(self, message)

        if message.content.startswith(prefix + 'stop'):
            await musicplayer.stop(self, message)

        if message.content.startswith(prefix + 'playlist'):
            await musicplayer.playlist(self, message)

        # GUESS GAME------------------------------
        if message.content.startswith(prefix + 'guess'):
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
        if message.content.startswith(prefix + 'quiz'):
            # Game Status updating
            now_playing = discord.Game(name='Trivia Quiz')
            await self.change_status(game=now_playing, idle=False)
            await triviagame.quiz(self, message)
            # Game Status updating
            now_playing = discord.Game(name='')
            await self.change_status(game=now_playing, idle=False)

        # OSU! API--------------------
        # TODO implement other osu!API Functions
        if message.content.startswith(prefix + 'stats'):
            my_string = message.content
            # osu module
            await self.send_message(message.channel, osu.stats(my_string))

        if message.content.startswith(prefix + 'top'):
            my_string = message.content
            await self.send_message(message.channel,
                                    'Fetching the requested data. Please wait...\n\n')
            # osu module
            await self.send_message(message.channel, osu.top(my_string))

        # 8 BALL----------------------
        if message.content.startswith(prefix + '8ball'):
            await eightball.main(self, message)

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')
        # Game Status updating
        now_playing = discord.Game(name='type ' + prefix + 'help for help')
        await self.change_status(game=now_playing, idle=False)


# email id and password loaded from config.yaml
emaild = doc['DISCORD_LOGIN']['email']
passwordd = doc['DISCORD_LOGIN']['password']
if passwordd is None:
    print('password cant be empty in config.yaml and must be within single quotes.')
    quit()
if emaild is None:
    print('email cant be empty in config.yaml and must be within single quotes.')
    quit()

try:
    bot = Bot()
    bot.run(emaild, passwordd)
except discord.LoginFailure:
    print('Your email or password in the config.yaml file are wrong.' +
          '\nCorrect them and try to run the bot again.')
    quit()
