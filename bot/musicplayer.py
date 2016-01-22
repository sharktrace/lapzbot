import json
import glob
import yaml
import subprocess as sp
import discord

async def load(self, message):
    await self.send_message(message.channel, 'Hooked to the voice channel. Please wait while'
                                             ' I populate the list of songs.')

    global s_playlist
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
        a = glob.glob('../audio_library/*.mp3')
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
    except FileExistsError as e:
        await self.send_message(message.channel,
                                '``' + str(e) + '```')

    s_playlist_dict = dict(s_playlist[i:i + 2] for i in range(0, len(s_playlist), 2))
    with open('../configuration/playListInfo.yaml', 'w') as f2:
        yaml.dump(s_playlist_dict, f2, default_flow_style=False)

    del s_playlist  # Deleting this variable cause already the data is dumped to playListInfo.yaml

    s_dict = dict(s_list[i:i + 2] for i in range(0, len(s_list), 2))

async def play(self, message):
    try:
        if self.player is not None and self.player.is_playing():
            await self.send_message(message.channel, '```Already playing a song. Please wait for current' +
                                    ' song to finish or use stop.```')
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

async def pause(self, message):
    try:
        if not self.is_voice_connected():
            await self.send_message(message.channel, '```Please connect to voice channel first```')

        if self.player.is_playing() == True and self.player.is_done() == False:
            await self.send_message(message.channel, 'Paused')

            self.player.pause()

    except Exception as e:
        await self.send_message(message.channel,
                                '```' + str(e) + '```')

async def resume(self, message):
    try:
        if not self.is_voice_connected():
            await self.send_message(message.channel, '```Please connect to voice channel first```')

        elif self.player.is_playing() == False and self.player.is_done() == False:
            await self.send_message(message.channel, 'Resumed')

            self.player.resume()

    except Exception as e:
        await self.send_message(message.channel,
                                '```' + str(e) + '```')

async def stop(self, message):
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

async def playlist(self, message):
    try:
        # Loading configurations from config.yaml
        with open('../configuration/playListInfo.yaml', 'r') as f3:
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
