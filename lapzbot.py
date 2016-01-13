import discord
import urllib.request
import json
import requests

client = discord.Client()
client.login('username', 'password')

@client.event
def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('{} hello'.format(client.user.mention())):
        client.send_message(message.channel, 'Hello {}'.format(message.author.mention()))

    if message.content.startswith('{} help'.format(client.user.mention())):
        client.send_message(message.channel, 'Hello {}, the following commands are available:- `hello`, `help`, `stats <username>`, `top <username>`, `wtf`'.format(message.author.mention()) +'\n'+'For stats <username> and top <username> make sure to use _(underscore) if your username contains 2 words or more. Example:- `@lapzbot stats John_Smith`')

    if message.content.startswith('{} wtf'.format(client.user.mention())):
        client.send_message(message.channel, 'WTF!!! {}, dont try to molest me. I am a kawaii little bot.'.format(message.author.mention()))
## osu! API functions-----------------------------------------------------------------------------------
    if message.content.startswith('{} stats'.format(client.user.mention())):
        my_string = message.content    
        splitted = my_string.split()
        first = splitted[0]
        second = splitted[1]
        third = splitted[2]

        r=requests.get('https://osu.ppy.sh/api/get_user?k=API Key&u='+third)
        data=r.json()
        for player in data:
            client.send_message(message.channel, 'Username : ' + player['username'] + '\n' + 'Performance Points : ' + "%.2f" % float(player['pp_raw']) + '\n' +  'Accuracy : ' + "%.2f" % float(player['accuracy']) + '\n' + 'Playcount : ' + player['playcount'] + '\n' +'Profile Link : https://osu.ppy.sh/u/'+player['user_id'])

    if message.content.startswith('{} top'.format(client.user.mention())):
        my_string = message.content    
        splitted = my_string.split()
        first = splitted[0]
        second = splitted[1]
        third = splitted[2]

        print(client.user)
        print(message.author)
        
        r=requests.get('https://osu.ppy.sh/api/get_user_best?k=API Key&u='+third+'&limit=5')
        data=r.json()
        msg = ''
        for player in data:
            thr = int(player['count300'])
            hun = int(player['count100'])
            fif = int(player['count50'])
            miss = int(player['countmiss'])
            tph = int(300*thr + 100*hun + 50*fif)
            tnh = int(thr + hun + fif + miss)
            acc = float(tph / (tnh*3))
            msg += str('Beatmap : ' + 'https://osu.ppy.sh/b/'+player['beatmap_id'] + ' | ' + 'Acc : ' + "%.2f" % float(acc) + ' | ' + 'Rank : ' + player['rank'] + ' | ' + 'PP : ' + player['pp'] + '\n')

        client.send_message(message.channel, msg)
        
## Chat Emotes--------------------------------------------------------------------------------------
    if message.content.startswith('!kappa'):
        client.send_message(message.channel, 'http://i.imgur.com/N5RzfBB.png')

    if message.content.startswith('!feelsbadman'):
        client.send_message(message.channel, 'http://i.imgur.com/DfURIfh.png')

    if message.content.startswith('!feelsgoodman'):
        client.send_message(message.channel, 'http://i.imgur.com/9Ggf2vs.png')

    if message.content.startswith('!lapz'):
        client.send_message(message.channel, 'http://i.imgur.com/I0Lqf3w.png')
        
@client.event
def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run()
