import discord
import json
import requests
import bs4
import time
import subprocess as sp
import glob
import random
import yaml

# Loading configurations from config.yaml
with open('./configuration/config.yaml', 'r') as f:
    doc = yaml.load(f)

# TODO Add support for 64 bit as well
if not discord.opus.is_loaded():
    discord.opus.load_opus('libopus-0.x86.dll')


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

        # Music Player codes---------------
        if message.content.startswith('!load'.format(self.user.mention)):
            await self.send_message(message.channel, 'Hooked to the voice channel. Please wait while'
                                                     ' I populate the list of songs.')

            global player, s_playlist
            global voice_stream

            if self.is_voice_connected():
                await self.send_message(message.channel,
                                        '```Discord API doesnt let me join multiple servers at the moment.```')

            else:
                voice_stream = await self.join_voice_channel(message.author.voice_channel)

            # TODO get a better way to store local playlist
            try:
                global ids  # The sole purpose for this is to be used with !playlist
                ids = 0
                global s_dict
                global s_list
                s_list = []
                s_playlist = []
                a = glob.glob('./audio_library/*.mp3')
                for a in a:
                    try:
                        b = a.replace('\\', '/')
                        ids += 1
                        s_list.append(ids)
                        s_list.append(b)
                        print(b)
                        p = sp.Popen(['ffprobe', '-v', 'quiet', '-print_format', 'json=compact=1', '-show_format',
                                      b], stdout=sp.PIPE, stderr=sp.PIPE)
                        op = p.communicate()
                        op_json = json.loads(op[0].decode('utf-8'))
                        title = op_json['format']['tags']['title']
                        artist = op_json['format']['tags']['artist']
                        await self.send_message(message.channel,
                                                title + ' - ' + artist + ' (code: **' + str(ids) + '**)')
                        s_playlist.append(ids)
                        s_playlist.append(title + ' - ' + artist)

                    except Exception as e:
                        print(str(e))
            except:
                await self.send_message(message.channel,
                                        '```No songs in the directory.```')

            s_playlist_dict = dict(s_playlist[i:i + 2] for i in range(0, len(s_playlist), 2))
            with open('./configuration/playListInfo.yaml', 'w') as f2:
                yaml.dump(s_playlist_dict, f2, default_flow_style=False)

            del s_playlist  # Deleting this variable cause already the data is dumped to playListInfo.yaml

            s_dict = dict(s_list[i:i + 2] for i in range(0, len(s_list), 2))

        if message.content.startswith('!play '):

            try:
                if self.player is not None and self.player.is_playing():
                    await self.send_message(message.channel, 'Already playing a song')
                    return
                else:
                    my_string = message.content
                    splitted = my_string.split()
                    second = int(splitted[1])

                    self.player = self.voice.create_ffmpeg_player(str(s_dict[second]))

                    # FFProbing for info
                    p = sp.Popen(['ffprobe', '-v', 'quiet', '-print_format', 'json=compact=1', '-show_format',
                                  str(s_dict[second])], stdout=sp.PIPE, stderr=sp.PIPE)
                    op = p.communicate()
                    op_json = json.loads(op[0].decode('utf-8'))
                    title = op_json['format']['tags']['title']
                    artist = op_json['format']['tags']['artist']
                    leng = op_json['format']['duration']
                    seconds = float(leng)
                    m, s = divmod(seconds, 60)
                    h, m = divmod(m, 60)
                    print('title:', title)
                    print('artist:', artist)
                    await self.send_message(message.channel, 'Currently playing **' + title + ' - ' + artist +
                                            '**. Song duration is **%d:%02d:%02d' % (h, m, s) + '**.')

                    # Game Status updating
                    now_playing = discord.Game(name=title)
                    await self.change_status(game=now_playing, idle=False)

                    self.player.start()

            except Exception as e:
                await self.send_message(message.channel,
                                        '```' + str(e) + '```')

        if message.content.startswith('!pause'):

            try:
                if not self.is_voice_connected():
                    await self.send_message(message.channel, '```Please connect to voice channel first```')

                if player.is_playing() == True and player.is_done() == False:
                    await self.send_message(message.channel, 'Paused')

                    now_playing = discord.Game(name='Paused')
                    await self.change_status(game=now_playing, idle=False)

                    self.player.pause()

            except Exception as e:
                await self.send_message(message.channel,
                                        '```' + str(e) + '```')

        if message.content.startswith('!resume'):

            try:
                if not self.is_voice_connected():
                    await self.send_message(message.channel, '```Please connect to voice channel first```')

                elif player.is_playing() == True and player.is_done() == False:
                    await self.send_message(message.channel, 'Paused')

                    now_playing = discord.Game(name='Paused')
                    await self.change_status(game=now_playing, idle=False)

                    self.player.resume()

            except Exception as e:
                await self.send_message(message.channel,
                                        '```' + str(e) + '```')

        if message.content.startswith('!stop'):

            try:
                if not self.is_voice_connected():
                    await self.send_message(message.channel, '```Please connect to voice channel first```')

                elif self.player.is_playing() == True and self.player.is_done() == False:
                    await self.send_message(message.channel, 'stopped')

                    now_playing = discord.Game(name='')
                    await self.change_status(game=now_playing, idle=False)

                    self.player.stop()

            except Exception as e:
                await self.send_message(message.channel,
                                        '```' + str(e) + '```')

        if message.content.startswith('!playlist'):

            try:
                # Loading configurations from config.yaml
                with open('./configuration/playListInfo.yaml', 'r') as f3:
                    plist = yaml.load(f3)
                idq = 1
                plistfinal = ''
                while idq <= ids:
                    song = plist[idq]
                    plistfinal += str(song + ' (code: **' + str(idq) + '**)\n')
                    idq += 1

                await self.send_message(message.channel, plistfinal)

            except Exception as e:
                await self.send_message(message.channel,
                                        '```' + str(e) + '```')

        # Yes/No API Codes---------
        if message.content.startswith('{} '.format(self.user.mention)):
            x = message.content
            if x.startswith('<@134962024324136960> is') or x.startswith('<@134962024324136960> are') or x.startswith(
                    '<@134962024324136960> will') or x.startswith('<@134962024324136960> do') or x.startswith(
                    '<@134962024324136960> would'):
                print(x)
                r = requests.get('http://yesno.wtf/api')
                data = r.json()
                await self.send_message(message.channel, data['answer'] + '\n' + data['image'])
            if x.startswith('<@134962024324136960> what') or x.startswith('<@134962024324136960> why') or x.startswith(
                    '<@134962024324136960> when') or x.startswith('<@134962024324136960> how') or x.startswith(
                    '<@134962024324136960> where'):
                print(x)
                await self.send_message(message.channel,
                                        'Oww, my creator has instructed me not to answer that question.' +
                                        ' Next question please...')

        # GUESSING GAME CODES---------
        if message.content.startswith('!guess'):

            # Game Status updating
            now_playing = discord.Game(name='Guessing Game')
            await self.change_status(game=now_playing, idle=False)

            await self.send_message(message.channel, 'Guess a number between 1 to 10')

            def guess_check(m1):
                return m1.content.isdigit()

            guess = await self.wait_for_message(timeout=5.0, author=message.author, check=guess_check)
            answer = random.randint(1, 10)
            if guess is None:
                fmt = 'Sorry, you took too long. It was {}.'
                await self.send_message(message.channel, fmt.format(answer))
                return
            if int(guess.content) == answer:
                await self.send_message(message.channel, 'You are right!')
            else:
                await self.send_message(message.channel, 'Sorry. It is actually {}.'.format(answer))

            # Game Status updating
            now_playing = discord.Game(name='')
            await self.change_status(game=now_playing, idle=False)

        # Trivia Quiz game codes-----------------
        # TODO the strings are not compared correctly. Need to fix.
        if message.content.startswith('!quiz'):
            # Game Status updating
            now_playing = discord.Game(name='Trivia Quiz')
            await self.change_status(game=now_playing, idle=False)

            r = requests.get('http://jservice.io/api/random?')
            data = r.json()

            for player in data:
                await self.send_message(message.channel, player['question'])

                guess = await self.wait_for_message(timeout=10.0, author=message.author)
                guess_l = str(guess).lower()
                answer = str(player['answer']).lower()
                set1 = set(guess_l.split(' '))
                set2 = set(answer.split(' '))
                if guess_l is None:
                    fmt = 'Sorry, you took too long. It was {}.'
                    await self.send_message(message.channel, fmt.format(answer))
                    return
                if set1 == set2:
                    await self.send_message(message.channel, 'You are right!')
                else:
                    await self.send_message(message.channel, 'Sorry. It is actually {}.'.format(answer))

            # Game Status updating
            now_playing = discord.Game(name='')
            await self.change_status(game=now_playing, idle=False)

        # OSU! API FUNCTIONS--------------------
        # TODO implement other osu!API Functions
        if message.content.startswith('!stats'):
            my_string = message.content
            splitted = my_string.split()
            third = splitted[1]

            # key loaded from config.yaml
            key = doc['OSU_API']['KEY']
            r = requests.get('https://osu.ppy.sh/api/get_user?k=' + key + '&u=' + third)
            data = r.json()
            for player in data:
                await self.send_message(message.channel,
                                        'https://a.ppy.sh/' + player['user_id'] + '\nUsername : ' + player[
                                            'username'] + '\nPerformance Points : ' + "%.2f" % float(
                                                player['pp_raw']) + '\nAccuracy : ' + "%.2f" % float(
                                                player['accuracy']) + '\nPlaycount : ' + player[
                                            'playcount'] + '\nProfile Link : `osu.ppy.sh/u/' + player['user_id'] + '`')

        if message.content.startswith('!top'):
            my_string = message.content
            splitted = my_string.split()
            third = splitted[1]

            await self.send_message(message.channel,
                                    'Fetching the requested data. Please wait...\n\n')
            start_time = time.time()

            # key loaded from config.yaml
            key = doc['OSU_API']['KEY']

            r = requests.get('https://osu.ppy.sh/api/get_user_best?k=' + key + '&u=' + third + '&limit=5')

            data = r.json()
            msg = ''
            for player in data:
                thr = int(player['count300'])
                hun = int(player['count100'])
                fif = int(player['count50'])
                miss = int(player['countmiss'])
                tph = int(300 * thr + 100 * hun + 50 * fif)
                tnh = int(thr + hun + fif + miss)
                acc = float(tph / (tnh * 3))

                # TODO work on parsing with LXML
                bitits = requests.get('https://osu.ppy.sh/b/' + player['beatmap_id'])
                html = bs4.BeautifulSoup(bitits.text, 'lxml')
                tits = html.title.text

                msg += str(
                        'Beatmap : ' + tits + ' `osu.ppy.sh/b/' + player[
                            'beatmap_id'] + '`' + '\n Acc : ' + "%.2f" % float(
                                acc) + ' | ' + 'Rank : ' + player['rank'] + ' | ' + 'PP : ' + player['pp'] + '\n')

            await self.send_message(message.channel, msg + '\nThis request took `' + "%.2f" % (
                time.time() - start_time) + ' seconds` to process.')

        # TODO get more Chat Emotes
        if message.content.startswith('!kappa'):
            await self.send_message(message.channel, 'http://i.imgur.com/N5RzfBB.png')

        if message.content.startswith('!feelsbadman'):
            await self.send_message(message.channel, 'http://i.imgur.com/DfURIfh.png')

        if message.content.startswith('!feelsgoodman'):
            await self.send_message(message.channel, 'http://i.imgur.com/9Ggf2vs.png')

        if message.content.startswith('!lapz'):
            await self.send_message(message.channel, 'http://i.imgur.com/I0Lqf3w.png')

    # async def on_member_update(before, after):
    #     bf_serv = before.server
    #     af_serv = after.server
    #     bf_status = before.status
    #     af_status = after.status
    #
    #     if bf_status == 'offline' and af_status == 'online':
    #         await self.send_message(af_serv, 'Wassup {0}, welcome back !'.format(after.mention))

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
